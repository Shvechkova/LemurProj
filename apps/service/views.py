from ctypes import cast
import datetime
from itertools import groupby
from math import sumprod
from django.forms import DateField

from rest_framework.decorators import action
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.db.models import Prefetch
from django.db.models import Func, F, Value
from django.db.models import F, Q

# from apps import service

from operator import itemgetter
from itertools import groupby


from apps.client.models import AdditionalContract, Client

from apps.operation.models import Operation, OperationEntry
from apps.service.forms import OperationEntryForm

from apps.service.models import Adv, Service, ServicesMonthlyBill, SubcontractMonth
from rest_framework import routers, viewsets
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework import status

from apps.service.serializers import ServiceSerializer


def index(request):
    title = "Услуги"
    context = {
        "title": title,
    }
    return render(request, "service/service.html", context)


def service_one(request, slug):
    # куки для установки дат сортировки
    if request.COOKIES.get('sortMonth'):
        month = request.COOKIES["sortMonth"]
    else:
        month = '1'

    category_service = Service.objects.get(name=slug)
    now = datetime.datetime.now()
    year = now.year

    # выбор периода сортировки
    if month == '1':
        old_month = now.month

    elif month == '2':
        old_month = now.month - 1
        if old_month == 0:
            old_month = 12
        year = now.year
        if old_month == 12:
            year = year - 1
    elif month == '3':
        old_month = now.month - 2
        if old_month == 0:
            old_month = 12
        year = now.year
        if old_month == 12:
            year = year - 1
    elif month == '12':
        old_month = 1
        year = now.year
    elif month == '999':
        old_month = 1
        year = 1990

    bill_now_mohth = (
        ServicesMonthlyBill.objects.filter(service=category_service)
        .annotate(month=TruncMonth("created_timestamp"))
        .filter(created_timestamp__year__gte=year, created_timestamp__month__gte=old_month)
        .select_related("client").order_by("-month"))

    # for bill in bill_now_mohth:
    #     print(bill)
    #     print(bill.month)
    suborders_name = Adv.objects.all()
    # bill_now_mohth = (
    #     ServicesMonthlyBill.objects.filter(service=category_service)
    #     .annotate(month=TruncMonth("created_timestamp"))
    #     .filter(created_timestamp__year=now.year, created_timestamp__month=now.month)
    #     .select_related("client")
    # )
    suborders_name_no_adv = SubcontractMonth.objects.filter(
        month_bill__service=category_service,
        created_timestamp__year__gte=year,
        created_timestamp__month__gte=old_month, other__isnull=False
    ).annotate(month=TruncMonth('created_timestamp')).values('month').annotate(total=Sum('amount', default=0)).values("other_id__name", "other_id__id", "month", 'total').order_by("other").distinct()
    # print(suborders_name_no_adv)
    total_month = ServicesMonthlyBill.objects.filter(
        service=category_service,
    ).annotate(month=TruncMonth('created_timestamp')).values('month').annotate(contract_sum=(
        Sum('contract_sum', default=0)
    ), adv_all_sum=(
        Sum('adv_all_sum', default=0)
    ), diff_sum=(
        Sum('diff_sum', default=0)
    )
    )

    operation = Operation.objects.filter(
        monthly_bill__service=category_service,
        data__year__gte=year,
        data__month__gte=old_month,
    ).select_related("bank").annotate(month=TruncMonth('data')).values('month', 'type_operation').annotate(total=Sum('amount', default=0), bank1=(
        Sum('amount', filter=Q(bank=1), default=0)
    ), bank2=(
        Sum('amount', filter=Q(bank=2), default=0)
    ), bank3=(
        Sum('amount', filter=Q(bank=3), default=0)
    )
    )

    diff_sum_oper = []
    for x in range(len(total_month)):
        obj = {}
        total_month[x]['total_diff_operation_entry'] = total_month[x]['contract_sum']
        total_month[x]['total_diff_operation_out'] = 0
        total_month[x]['total_diff_operation_out_adv'] = total_month[x]['diff_sum']
        total_month[x]['sum_entry_operation'] = 0
        total_month[x]['sum_out_operation'] = 0
        for y in range(len(operation)):

            if total_month[x]['month'] == operation[y]['month']:

                if operation[y]['type_operation'] == 'entry':
                    total_month[x]['sum_entry_operation'] = operation[y]['total']
                    total_diff_operation_entry = total_month[x]['contract_sum'] - \
                        operation[y]['total']
                    total_month[x]['total_diff_operation_entry'] = total_diff_operation_entry
                    total_month[x]['bank1_entry'] = operation[y]['bank1']
                    total_month[x]['bank2_entry'] = operation[y]['bank2']
                    total_month[x]['bank3_entry'] = operation[y]['bank3']

                if operation[y]['type_operation'] == 'out':
                    total_month[x]['sum_out_operation'] = operation[y]['total']
                    total_diff_operation_out = total_month[x]['diff_sum'] - \
                        operation[y]['total']
                    total_month[x]['total_diff_operation_out'] = total_diff_operation_out
                    total_month[x]['bank1_out'] = operation[y]['bank1']
                    total_month[x]['bank2_out'] = operation[y]['bank2']
                    total_month[x]['bank3_out'] = operation[y]['bank3']

        diff_sum_oper.append(obj)

    obj_suborder_adv = []
    obj_suborder_other = []

    # if slug == 'ADV':
    #     suborders_name_item = suborders_name
    # else:
    #     suborders_name_item = suborders_name_no_adv

    if slug == 'ADV':
        suborder_total_other = SubcontractMonth.objects.filter(
            month_bill__service=category_service,
            created_timestamp__year__gte=year, created_timestamp__month__gte=old_month, other__isnull=False
        ).annotate(month=TruncMonth('created_timestamp')).values('month').annotate(total_amount=(
            Sum('amount', default=0)))

        obj_suborder_other.append(suborder_total_other)

        for subs_item in suborders_name:
            suborder_total = SubcontractMonth.objects.filter(
                month_bill__service=category_service,
                created_timestamp__year__gte=year,
                created_timestamp__month__gte=old_month, adv=subs_item.id
            ).annotate(month=TruncMonth('created_timestamp')).values('month', 'adv__name').annotate(total_amount=(
                Sum('amount', default=0)))

            obj_suborder_adv.append(suborder_total)

    else:
        suborder_total_other = SubcontractMonth.objects.filter(
            month_bill__service=category_service,
            created_timestamp__year__gte=year, created_timestamp__month__gte=old_month, other__isnull=False
        ).annotate(month=TruncMonth('created_timestamp')).values('month').annotate(total_amount=(
            Sum('amount', default=0)))

        for x in range(len(total_month)):
            for y in range(len(suborder_total_other)):

                if total_month[x]['month'] == suborder_total_other[y]['month']:

                    total_month[x]['total_suborder_not_adv'] = suborder_total_other[y]['total_amount']
                    total_month[x]['total_suborder_not_adv_diff'] = 0

                    if suborder_total_other[y]['total_amount']:
                        total_month[x]['total_suborder_not_adv_diff'] = suborder_total_other[y]['total_amount'] - \
                            total_month[y]['sum_out_operation']

        for subs_item in suborders_name_no_adv:
            name = {
                # "name_adv": subs_item['other_id__name'],
                # "id_adv": subs_item['other_id__id'],
            }
            suborder_total = SubcontractMonth.objects.filter(
                month_bill__service=category_service,
                created_timestamp__year__gte=year, created_timestamp__month__gte=old_month, other=subs_item[
                    'other_id__id']
            ).annotate(month=TruncMonth('created_timestamp')).values('month', "amount").values("other_id__name", "other_id__id", "month", 'amount').aggregate(total_amount=Sum('amount'))

            # name['total_amount'] = suborder_total['total_amount']
            # name['month'] = suborder_total['month']
            # name['other_id__name'] = suborder_total['other_id__name']
            # obj_suborder_adv.append(name)
            # print(subs_item)

    title = category_service.id
    context = {
        "title": title,
        "category_service": category_service,

        "bills": bill_now_mohth,
        "now": now,
        "suborders_name": suborders_name,

        "obj_suborder_adv": obj_suborder_adv,
        # "suborder_total_other": suborder_total_other,
        "suborders_name_no_adv": suborders_name_no_adv,
        "operation": operation,
        "total_month": total_month,
        "diff_sum_oper": diff_sum_oper,
        "obj_suborder_other": obj_suborder_other

    }
    return render(request, "service/one_service.html", context)


def new_month(request):
    now = datetime.datetime.now()

    old_month = now.month - 1
    if old_month == 0:
        old_month = 12
    year = now.year
    if old_month == 12:
        year = year - 1

    bill_now_old = ServicesMonthlyBill.objects.filter(
        created_timestamp__year=year, created_timestamp__month=old_month)

    for old_bill in bill_now_old:
        subcontr_old = SubcontractMonth.objects.filter(month_bill=old_bill.id)

        new_bill = old_bill
        new_bill.pk = None
        new_bill.save()
        if subcontr_old.exists():
            for subs_old in subcontr_old:

                new_subs = subs_old
                new_subs.pk = None
                new_subs.month_bill_id = new_bill.id

                new_subs.save()
                new_bill_qurery = ServicesMonthlyBill.objects.filter(
                    id=new_bill.id).update(chekin_add_subcontr=True)
                # new_bill.update(chekin_add_subcontr=True)

    context = {
        "title": 1,
    }

    return render(request, "service/service.html", context)
