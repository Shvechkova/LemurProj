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

# from apps.service.serializers import ClientAllSerializer, ContractSerializer
from rest_framework import status

from apps.service.serializers import ServiceSerializer


def index(request):
    # month_bill_all = ServicesMonthlyBill.objects.all()
    title = "Услуги"
    context = {
        "title": title,
        # "month_bill_all": month_bill_all,
    }
    return render(request, "service/service.html", context)


def service_one(request, slug):
    #куки для установки дат сортировки
    if request.COOKIES.get('sortMonth'):
        month = request.COOKIES["sortMonth"]
        
    else:
        month = 1
        
  
    category_service = Service.objects.get(name=slug)

    # ordered_bill = ServicesMonthlyBill.objects.filter(service=category_service).order_by("-created_timestamp")
    # ordered_bill = ServicesMonthlyBill.objects.filter(service=category_service).prefetch_related('additional_contract',"client").order_by("-created_timestamp")

    # total_income = ServicesMonthlyBill.get_total_income(category_service)
    # total_adv = ServicesMonthlyBill.get_total_income_adv(category_service)

    # total_sub = ServicesMonthlyBill.get_total_income_suborder(category_service)

    # subcontractors = SubcontractMonth.objects.all()
    # operation_entry = OperationEntry.objects.all()
    # advCategory = Adv.objects.all()

    # bill = (
    #     ordered_bill.annotate(month=TruncMonth(
    #     'created_timestamp')).values('month').annotate(total_amount=Sum('additional_contract__adv_all_sum'))
    #     )

    # print(bill)
    # total_sub_adv = (
    #         ordered_bill.all().annotate(total_amount=Sum('subcontractmonth__amount'))
    #     )
    #     .prefetch_related('operation_set').all()
    # print(bill_now_mohth)

    # bill_all_mohth = ServicesMonthlyBill.objects.filter(service=category_service).annotate(month=TruncMonth(
    #     'created_timestamp')).prefetch_related("subcontract") 
    
    now = datetime.datetime.now()
    # old_month = now.month - 1
    # if old_month == 0 :
    #     old_month = 12
    # year = now.year
    # if old_month == 12 :
    #     year = year - 1
        
    # # date_need =    
        
    # print(old_month,year)  
      
    # выбор периода сортировки 
    if month == '1':
        old_month = now.month
        year = now.year
    #      bill_now_mohth = (
    #     ServicesMonthlyBill.objects.filter(service=category_service)
    #     .annotate(month=TruncMonth("created_timestamp"))
    #     .filter(created_timestamp__year=now.year, created_timestamp__month=now.month)
    #     .select_related("client")
    # )
        
      
    elif month == '2': 
        old_month = now.month - 1
        if old_month == 0 :
            old_month = 12
        year = now.year
        if old_month == 12 :
            year = year - 1
    elif month == '3':
        old_month = now.month - 2
        if old_month == 0 :
            old_month = 12
        year = now.year
        if old_month == 12 :
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
        .select_related("client").order_by("-month") )   
  
        
       
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
        created_timestamp__year=now.year,
        created_timestamp__month=now.month,other__isnull=False
    ).values("other_id__name","other_id__id").order_by("other").distinct()
    
    total_month = ServicesMonthlyBill.objects.filter(
        service=category_service,
    ).annotate(month=TruncMonth('created_timestamp')).values('month').annotate( contract_sum=(
        Sum('contract_sum',default=0)
    ),adv_all_sum=(
        Sum('adv_all_sum',default=0)
    ),diff_sum=(
        Sum('diff_sum',default=0)
    )
)
  

    total_month_contract_sum = 0
    total_month_adv_all_sum = 0
    total_month_diff_sum = 0

    for bill in bill_now_mohth:
        total_month_contract_sum += bill.contract_sum
        total_month_adv_all_sum += bill.adv_all_sum
        total_month_diff_sum += bill.diff_sum

    operation = Operation.objects.filter(
        monthly_bill__service=category_service,
         data__year__gte=year,
         data__month__gte=old_month,
    ).select_related("bank").annotate(month=TruncMonth('data')).values('month','type_operation').annotate(total=Sum('amount',default=0), bank1=(
        Sum('amount', filter=Q(bank=1),default=0)
    ),bank2=(
        Sum('amount', filter=Q(bank=2),default=0)
    ),bank3=(
        Sum('amount', filter=Q(bank=3),default=0)
    )
)
    print(operation)
    diff_sum_oper = []
    for x in range(len(total_month)):
            obj={}
            total_month[x]['total_diff_operation_entry'] = total_month[x]['contract_sum'] 
            total_month[x]['total_diff_operation_out'] = 0
            total_month[x]['sum_entry_operation'] = 0
            for y in range(len(operation)): 
                
                if total_month[x]['month'] == operation[y]['month']:
                    
                    if  operation[y]['type_operation'] == 'entry':  
                        total_month[x]['sum_entry_operation'] = operation[y]['total']  
                        total_diff_operation_entry = total_month[x]['contract_sum'] - operation[y]['total']
                        total_month[x]['total_diff_operation_entry'] = total_diff_operation_entry
                        # obj['total_diff_operation_entry']=total_diff_operation_entry
                        # obj['total_month']=operation[y]['month']
                        
                    if  operation[y]['type_operation'] == 'out':  
                        total_month[x]['sum_out_operation'] = operation[y]['total']     
                        total_diff_operation_out = total_month[x]['diff_sum'] - operation[y]['total']
                        total_month[x]['total_diff_operation_out'] = total_diff_operation_out
                        # obj['total_diff_operation_out']=total_diff_operation_out
                        # obj['total_month']=operation[y]['month']
                   
                        
                   
            diff_sum_oper.append(obj)
                    
      
    
         
    # .values('month','type_operation',"amount",'id',"bank").order_by("month")
 
    total_sum_all_operation_entry = 0
    total_sum_operation_entry_bank1 = 0
    total_sum_operation_entry_bank2 = 0
    total_sum_operation_entry_bank3 = 0
 
    # for oper in operation:
    #     if oper['type_operation'] == "entry":
    #         total_sum_all_operation_entry += oper['amount']

    #         if oper['bank'] == 1:
    #             total_sum_operation_entry_bank1 += oper['amount']

    #         elif oper['bank']== 2:
    #             total_sum_operation_entry_bank2 += oper['amount']
    #         elif oper['bank'] == 3:
    #             total_sum_operation_entry_bank3 += oper['amount']

    total_sum_all_operation_out = 0
    total_sum_operation_out_bank1 = 0
    total_sum_operation_out_bank2 = 0
    total_sum_operation_out_bank3 = 0

    # for oper_out in operation:
    #     if oper_out.type_operation == "out":
    #         total_sum_all_operation_out += oper_out.amount

    #         if oper_out.bank.id == 1:
    #             total_sum_operation_out_bank1 += oper_out.amount

    #         elif oper_out.bank.id == 2:
    #             total_sum_operation_out_bank2 += oper_out.amount
    #         elif oper_out.bank.id == 3:
    #             total_sum_operation_out_bank3 += oper_out.amount

    # total_diff_operation_entry = (
    #     total_month_contract_sum - total_sum_all_operation_entry
    # )

   
    if slug == "ADV":
        total_diff_operation_out = total_month_diff_sum - total_sum_all_operation_out
    else:
        suborder_total_other = SubcontractMonth.objects.filter(
        month_bill__service=category_service,
        created_timestamp__year=now.year,
        created_timestamp__month=now.month,other__isnull=False
    ).aggregate(total_amount=Sum('amount',default=0))
        
        total_diff_operation_out = suborder_total_other["total_amount"] - total_sum_all_operation_out
   
    total_oper = [
        {
            "total_sum_all_operation_entry": total_sum_all_operation_entry,
            # "total_diff_operation_entry": total_diff_operation_entry,
            "total_sum_operation_entry_bank1": total_sum_operation_entry_bank1,
            "total_sum_operation_entry_bank2": total_sum_operation_entry_bank2,
            "total_sum_operation_entry_bank3": total_sum_operation_entry_bank3,
            "total_sum_all_operation_out": total_sum_all_operation_out,
            # "total_diff_operation_out": total_diff_operation_out,
            "total_sum_operation_out_bank1": total_sum_operation_out_bank1,
            "total_sum_operation_out_bank2": total_sum_operation_out_bank2,
            "total_sum_operation_out_bank3": total_sum_operation_out_bank3,
        }
    ]

    obj_suborder_adv = []

    if slug == 'ADV':
        suborders_name_item = suborders_name
    else:
       suborders_name_item = suborders_name_no_adv

    for subs_item in suborders_name_item:
        # name = {
        #     "name_adv": subs_item.name,
        #     "id_adv": subs_item.id,
        # }
        if slug == 'ADV':
       
            name = {
                "name_adv": subs_item.name,
                "id_adv": subs_item.id,
            }
            suborder_total = SubcontractMonth.objects.filter(
            month_bill__service=category_service,
            created_timestamp__year=now.year,
            created_timestamp__month=now.month,adv=subs_item.id
        ).aggregate(total_amount=Sum('amount'))
            name['total_amount'] = suborder_total['total_amount']
            obj_suborder_adv.append(name)
        else:
      
            name = {
                "name_adv": subs_item['other_id__name'],
                "id_adv": subs_item['other_id__id'],
            } 
            suborder_total = SubcontractMonth.objects.filter(
            month_bill__service=category_service,
            created_timestamp__year=now.year,
            created_timestamp__month=now.month,other=subs_item['other_id__id']
        ).aggregate(total_amount=Sum('amount'))
            name['total_amount'] = suborder_total['total_amount']
            obj_suborder_adv.append(name)   
        
       
        
        suborder_total_other = SubcontractMonth.objects.filter(
        month_bill__service=category_service,
        created_timestamp__year=now.year,
        created_timestamp__month=now.month,other__isnull=False
    ).aggregate(total_amount=Sum('amount',default=0))
        
        


    title = category_service.id
    context = {
        "title": title,
        "category_service": category_service,
        # "ordered_bill": ordered_bill,
        # 'total_income': total_income,
        # 'total_adv': total_adv,
        # 'subcontractors': subcontractors,
        # 'adv_category': advCategory,
        # 'operation_entry': operation_entry,
        "bills": bill_now_mohth,
        "now": now,
        "suborders_name": suborders_name,
        "total_month_contract_sum": total_month_contract_sum,
        "total_month_adv_all_sum": total_month_adv_all_sum,
        "total_month_diff_sum": total_month_diff_sum,
        "total_oper": total_oper,
        "obj_suborder_adv": obj_suborder_adv,
        "suborder_total_other": suborder_total_other,
        "suborders_name_no_adv": suborders_name_no_adv,
        "operation": operation,
        "total_month":total_month,
        "diff_sum_oper":diff_sum_oper
        
    }
    return render(request, "service/one_service.html", context)

def new_month(request):
    now = datetime.datetime.now()
    
    old_month = now.month - 1
    if old_month == 0 :
        old_month = 12
    year = now.year
    if old_month == 12 :
        year = year - 1
        
  
    
    bill_now_old =ServicesMonthlyBill.objects.filter(created_timestamp__year=year, created_timestamp__month=old_month)
    
    
    for old_bill in bill_now_old:
        subcontr_old =SubcontractMonth.objects.filter(month_bill=old_bill.id)
        print(subcontr_old)
        new_bill = old_bill
        new_bill.pk = None
        new_bill.save()
        if subcontr_old.exists():
            for subs_old in subcontr_old:
                print(subs_old)
                new_subs = subs_old
                new_subs.pk = None
                new_subs.month_bill_id = new_bill.id
                print(new_subs)
                new_subs.save()
                new_bill_qurery =ServicesMonthlyBill.objects.filter(id=new_bill.id).update(chekin_add_subcontr=True)
                # new_bill.update(chekin_add_subcontr=True)
                
            
    
    
    
    
    
    
    
    
    
    
    
    context = {
        "title": 1,
    }
    
    
    
    return render(request, "service/service.html", context)