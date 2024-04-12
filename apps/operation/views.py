from django.shortcuts import render
from rest_framework import routers, serializers, viewsets, mixins, status
from django.forms import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.operation.api.serializers import OperationEntrySerializer

from apps.operation.models import BankOperation, OperAccountsName, Operation, OperationEntry
from django.core.cache import cache
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.db.models import Prefetch
from django.db.models import Func, F, Value
from django.db.models import F, Q

from datetime import datetime
from dateutil.relativedelta import relativedelta

from apps.service.models import Service, ServiceClient

# Create your views here.


# общая функция кешировани
def loc_mem_cache(key, function, timeout=300):
    cache_data = cache.get(key)
    if not cache_data:
        cache_data = function()
        cache.set(key, cache_data, timeout)
    return cache_data


# внешние счета
def operation_outside(request):
    title = "внешние счета"

    # category_operation = [
    #     {"name": 'OOO',
    #      "tag": 'OOO',

    #      }, {
    #         "name": 'ИП',
    #         "tag": 'IP',
    #     }, {
    #         "name": '$',
    #         "tag": 'Nal',
    #     }]
    context = {
        "title": title,
        # "category_operation": category_operation,
    }
    return render(request, "operation/operation_outside.html", context)


# внешние счета подкатегории
def operation_outside_categ(request, slug):
    title = "CATEG"

    # category_operation = [
    #     {"name": 'OOO',
    #      "tag": 'OOO',

    #      }, {
    #         "name": 'ИП',
    #         "tag": 'IP',
    #     }, {
    #         "name": '$',
    #         "tag": 'Nal',
    #     }]

    # bank_operation = BankOperation.objects.get(slugish=slug)
    # service_category = Service.objects.all()
    # operation_in_servise = []

    # for service_categorys in service_category:
    #     operation = Operation.objects.filter(
    #         bank=bank_operation.id, monthly_bill__service__name=service_categorys.name, type_operation="entry").annotate(
    #         month=TruncMonth('created_timestamp')).values("month").annotate(sum=(
    #             Sum('amount', default=0)
    #         )).values("month", "sum")
    #     categor_servise = {
    #         "name":  service_categorys.name,
    #         'operation': operation
    #     }
    #     operation_in_servise.append(categor_servise)

    # print(operation_in_servise)
    # массив со всеми операциями и разницами сумм
    # diff_sum_oper = []
    # for x in range(len(total_month_entry)):
    #     obj = {}
    #     for y in range(len(operation_in_servise)):

    # total_month_entry = Operation.objects.all().annotate(month=TruncMonth('created_timestamp')).values('month').annotate(total_amount=(
    #     Sum('amount', default=0)
    # )).values('month')

    # operation = Operation.objects.filter(
    #     bank=bank_operation.id)

    # print(operation)
    # month_sum = []

    # for x in range(len(total_month_entry)):
    #     obj = {}
    #     total_month_entry[x]['sum_cat_entry'] = 0
    #     for y in range(len(operation)):
    #         if total_month_entry[x]['month'] == operation[y]['month']:
    #             if operation[y]['type_operation'] == 'entry':
    #                 total_month_entry[x]['sum_cat_entry'] += operation[y]['amount']
    #     month_sum.append(obj)

    # print(total_month_entry)

    # operations = Operation.objects.filter(bank=bank_operation.id, type_operation='entry').annotate(
    #     month=TruncMonth('created_timestamp')).annotate(service="monthly_bill__service_name").values('month', 'type_operation', 'amount',"service")

    context = {
        "title": title,
        # "category_operation": category_operation,
        # "operations": operation,
        # "bank_operation": bank_operation,
        # "service_category": service_category,
        # "total_month_entry": total_month_entry,
        # "operation_in_servise": operation_in_servise,

    }
    return render(request, "operation/operation_outside_categ.html", context)


# внутренние счета
def operation_inside(request):
    title = "внутренние счета"

    category_operation = [
        {"name": 'Оперсчет',
         "tag": 'oper_storage',

         }, {
            "name": 'Налоги',
            "tag": 'taxes',
        }, {
            "name": 'Банк.расходы',
            "tag": 'bank_expens',
        }]
    context = {
        "title": title,
        "category_operation": category_operation,
    }
    return render(request, "operation/operation_inside.html", context)


# внутренние счета категории
def operation_inside_categ(request, slug):
    title = "inside"
    category_operation = [
        {"name": 'Оперсчет',
         "tag": 'oper_storage',

         }, {
            "name": 'Налоги',
            "tag": 'taxes',
        }, {
            "name": 'Банк.расходы',
            "tag": 'bank_expens',
        }]

    total_month_entry = Operation.objects.all().annotate(month=TruncMonth('created_timestamp')).values('month').annotate(total_amount=(
        Sum('amount', default=0)
    )).values('month')

    if slug == 'oper_stor':
        category_oper = OperAccountsName.objects.all()
        cat_oper = []
        for category in category_oper:
            print(category.name)
            cat_oper.append(category.name)

    context = {
        "title": title,
        "category_operation": category_operation,
        "total_month_entry": total_month_entry,
        "cat_oper": cat_oper
    }
    return render(request, "operation/operation_inside_categ.html", context)


# внут счет оперсчет
def operation_inside_oper_account(request):
    title = "34534534"
    dateYearNow = datetime.now().year
    dateMonthNow = datetime.now().month
    print (dateYearNow, dateMonthNow)
    
    # dateYearNow = datetime(текущий_год, текущий_месяц, 1)

    context = {
        "title": title,
    }
    return render(request, "operation/operation_inside_oper_acount.html", context)


# налоги
def operation_inside_nalog(request):
    title = "34534534"

    context = {
        "title": title,
    }
    return render(request, "operation/operation_inside_nalog.html", context)


# банк операции
def operation_inside_bank(request):
    title = "34534534"

    context = {
        "title": title,
    }
    return render(request, "operation/operation_inside_bank.html", context)


# зарплаты
def operation_inside_salary(request):
    title = "34534534"

    context = {
        "title": title,
    }
    return render(request, "operation/operation_inside_salary.html", context)


# хранилище
def operation_storage(request):
    title = "хранилище"
    context = {
        "title": title,
    }
    return render(request, "operation/operation_storage.html", context)


# общая страница
def index(request):

    title = ""
    context = {

        "title": title,

    }
    return render(request, context)
