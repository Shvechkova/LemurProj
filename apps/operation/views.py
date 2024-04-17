from django.shortcuts import render
from rest_framework import routers, serializers, viewsets, mixins, status
from django.forms import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response


from apps.operation.models import BankOperation, CategoryOperation, OperAccountsName, Operation, SubCategoryOperation
from django.core.cache import cache
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth, TruncYear
from django.db.models import Prefetch
from django.db.models import Func, F, Value
from django.db.models import F, Q
from itertools import groupby
from operator import attrgetter

from datetime import datetime
import calendar
import locale
from dateutil.relativedelta import relativedelta

from apps.service.models import Service, ServiceClient

months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
          "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

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
    # даты
    data = datetime.now()
    year_now = datetime.now().year
    month_now = datetime.now().month
    # категории операций орперсчета

    def category_operation_cache():
        def cache_function():
            category_operation = CategoryOperation.objects.filter(
                meta_categ='oper_account').select_related("sub_categ").values("sub_categ", "meta_categ", 'name', "sub_categ__name", 'id')
            return category_operation

        return loc_mem_cache('category_operation', cache_function, 200)
    category_operation = category_operation_cache()

    # актуальные месяца нынешнего года
    month_names = []
    for month in range(1, month_now+1):
        month_name = months[month - 1]

        month_names.append({
            "name_month": month_name,
            "month": month,
        })
    month_names.reverse()
    # все месяца
    operation = Operation.objects.filter(meta_categ='oper_account', created_timestamp__year=year_now,
                                         created_timestamp__month__lte=month_now).select_related("category").annotate(month=TruncMonth('created_timestamp')).values('month').values("category", "month", 'amount', "id", "comment", "created_timestamp", "category__sub_categ__name").order_by('month')
    
    o = Operation.objects.filter(meta_categ='oper_account')
    result = {
    k: list(vs)
    for k, vs in groupby(o, attrgetter('category'))
    }
    print (result)
    
 
    # # глобальные подкатегории по оперсчет
    sub_category_operation = SubCategoryOperation.objects.filter(
        meta_categ=4)

    name_categ_list = []
    for name_categ in category_operation:
        name_categ_list.append({
            "category_operation_sub_categ": name_categ['sub_categ__name'],
            "category_operation_name": name_categ['name'],
            "category_operation_sub_categ_id": name_categ['id'],
            "category_operation_id": name_categ['sub_categ'],
        })

    # массив с категориями
    name_sub_categ_list = []
    for name_sub_categ in sub_category_operation:
        name_sub_categ_list.append({
            "category_sub_categ": name_sub_categ.name,
            "category_sub_categ_id": name_sub_categ.id,
        })

    # сборка пустых заготовок для оперецаям по месяцам и категориям
    dataset = []
    # по колиству актуальных месяцов
    for mont in range(1, month_now+1):
        # для тоталов по субкатегориям мес
        for v in name_sub_categ_list:
            months_act = {
                "month": mont,
                "month_name": months[mont - 1],
                "total_month": 0,
                "total_month_tag": 0,
                "sub_categ": v['category_sub_categ'],
                "sub_categ_id": v['category_sub_categ_id']
            }
            dataset.append(months_act)
        #  для каждого мес категорий месяцов
        for cat in name_categ_list:
            category_operations = {
                "month": mont,
                "month_name": months[mont - 1],
                "category_operation_sub_categ": cat['category_operation_sub_categ'],
                "category_operation_name": cat['category_operation_name'],
                "category_operation_id": cat['category_operation_sub_categ_id'],
                "total_month_tag": 1,
            }
            dataset.append(category_operations)


#    операции за актуальный год по месяцам
    for x in range(len(dataset)):
        dataset[x]['total'] = 0
        dataset[x]['id_operation'] = ""
        dataset[x]['comments'] = []
        dataset[x]['year_now'] = year_now
        dataset[x]['absolute_total_month'] = 0
        dataset[x]['total_month'] = 0

        for y in range(len(operation)):
            # сборка тоталов
            if dataset[x]['total_month_tag'] == 0:
                if dataset[x]['year_now'] == operation[y]['created_timestamp'].year and dataset[x]['month'] == operation[y]['month'].month and dataset[x]['sub_categ'] == operation[y]['category__sub_categ__name']:
                    dataset[x]['total_month'] = dataset[x]['total_month'] + \
                        operation[y]['amount']
            # сборка месяных по категориям
            else:
                if dataset[x]['year_now'] == operation[y]['created_timestamp'].year and dataset[x]['month'] == operation[y]['month'].month and dataset[x]['category_operation_id'] == operation[y]['category']:
                    dataset[x]['total'] = dataset[x]['total'] + \
                        operation[y]['amount']
                    dataset[x]['absolute_total_month'] = dataset[x]['absolute_total_month'] + \
                        operation[y]['amount']
                    dataset[x]['year'] = operation[y]['created_timestamp'].year
                    dataset[x]['id_operation'] = dataset[x]['id_operation'] + \
                        str(operation[y]['id']) + "-"
                    # комментарии к операциям
                    if operation[y]['comment']:
                        comment = {
                            "data": operation[y]['created_timestamp'],
                            "sum": operation[y]['amount'],
                            "comment": operation[y]['comment'],
                            #  "name":oper.suborder.name,
                        }
                        dataset[x]['comments'].append(comment)

    dataset.reverse()

    def old_oper(request):
        # operation_old_year = Operation.objects.filter(meta_categ='oper_account').order_by("-created_timestamp").last()
        # count_year = year_now - operation_old_year.created_timestamp.year
        # print(count_year)

        operation_old_year = Operation.objects.filter(meta_categ='oper_account', created_timestamp__year__lt=year_now).annotate(
            year=TruncYear('created_timestamp')).values('year')


        def operation_old_operation_cache():
            def cache_function():
                operation_old = Operation.objects.filter(meta_categ='oper_account', created_timestamp__year__lt=year_now).select_related("category").annotate(month=TruncMonth(
                    'created_timestamp')).values('month').values("category", "month", 'amount', "id", "comment", "created_timestamp", "category__sub_categ__name").order_by('month')
                return operation_old

            return loc_mem_cache('operation_old', cache_function, 200)
        operation_old = operation_old_operation_cache()
        
        year_operation_all = []
        i = 0
        month_arr = {}
        set = {}
        t = 0
        for cati in name_categ_list:
           
            category_operations = {
               
                "category_operation_sub_categ": cati['category_operation_sub_categ'],
                "category_operation_name": cati['category_operation_name'],
                "category_operation_id": cati['category_operation_sub_categ_id'],
                "total_month_tag": 1,
            }
            set[t] = category_operations
        for m in months:
            i += 1
            month = {
                "month_name": m,
                "month_count": i
            }
            
           
            month_arr[i] = month
      
        for years in operation_old_year:
            arr = {
                'year': years['year'].year,
                'months':month_arr
            }
            
            # month = {
            #     'month': "fff"
            # }
            year_operation_all.append(arr)
         

        print(year_operation_all)
        

        # i = 0
        # for m in months:
        #     i += 1
        #     month = {
        #         "month_name": m,
        #         "month_count": i
        #     }
        #     month_arr[i] = month

      
        # самая старая операция
    old_oper(request)

    # for old in operation_old_year:
    #     old_year = old.created_timestamp.year

    # print(old_year)
    context = {

        "category_operation": category_operation,
        "month_names": month_names,
        "dataset": dataset,
        "data": data,
        "year_now": year_now,



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
