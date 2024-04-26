
from django.shortcuts import render
from rest_framework import routers, serializers, viewsets, mixins, status
from django.forms import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response


from apps import employee
from apps.employee.models import Employee
from apps.operation.models import BankOperation, CategoryOperation, OperAccountsName, Operation, SubCategoryOperation
from django.core.cache import cache
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth, TruncYear
from django.db.models import Prefetch
from django.db.models import Func, F, Value
from django.db.models import F, Q
from itertools import groupby
from operator import attrgetter, length_hint

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

    context = {
        "title": title,

    }
    return render(request, "operation/operation_outside.html", context)


# внешние счета подкатегории
def operation_outside_categ(request, slug):
    title = "CATEG"

    context = {
        "title": title,


    }
    return render(request, "operation/operation_outside_categ.html", context)


# внутренние счета
def operation_inside(request):
    title = "внутренние счета"

    context = {
        "title": title,

    }
    return render(request, "operation/operation_inside.html", context)


# внутренние счета категории
def operation_inside_categ(request, slug):
    title = "inside"

    total_month_entry = Operation.objects.all().annotate(month=TruncMonth('created_timestamp')).values('month').annotate(total_amount=(
        Sum('amount', default=0)
    )).values('month')

    if slug == 'oper_stor':
        category_oper = OperAccountsName.objects.all()
        cat_oper = []
        for category in category_oper:

            cat_oper.append(category.name)

    context = {
        "title": title,

        "total_month_entry": total_month_entry,
        "cat_oper": cat_oper
    }
    return render(request, "operation/operation_inside_categ.html", context)


# внут счет оперсчет
def operation_inside_oper_account(request):
    type_url = 'operation_inside'
    # даты
    data = datetime.now()
    year_now = datetime.now().year
    month_now = datetime.now().month
    # куки для сортировки
    if request.COOKIES.get('sortOperAccount') and request.COOKIES.get('sortOperAccount') != "0":
        bank_id = request.COOKIES["sortOperAccount"]

        operation = Operation.objects.filter(meta_categ='oper_account', created_timestamp__year=year_now, created_timestamp__month__lte=month_now, bank=bank_id).select_related("category").annotate(
            month=TruncMonth('created_timestamp')).values('month').values("category", "month", 'amount', "id", "comment", "created_timestamp", "category__sub_categ__name").order_by('month')

        operation_old = operation_old = Operation.objects.filter(meta_categ='oper_account', created_timestamp__year__lt=year_now, bank=bank_id).select_related("category").annotate(month=TruncMonth(
            'created_timestamp')).values('month').values("category", "month", 'amount', "id", "comment", "created_timestamp", "category__sub_categ__name", "category__sub_categ__id").order_by('month')

    else:
        bank_id = '0'
        operation = Operation.objects.filter(meta_categ='oper_account', created_timestamp__year=year_now, created_timestamp__month__lte=month_now).select_related("category").annotate(
            month=TruncMonth('created_timestamp')).values('month').values("category", "month", 'amount', "id", "comment", "created_timestamp", "category__sub_categ__name").order_by('month')
        operation_old = Operation.objects.filter(meta_categ='oper_account', created_timestamp__year__lt=year_now).select_related("category").annotate(month=TruncMonth(
            'created_timestamp')).values('month').values("category", "month", 'amount', "id", "comment", "created_timestamp", "category__sub_categ__name", "category__sub_categ__id").order_by('month')

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
    # operation = Operation.objects.filter(meta_categ='oper_account', created_timestamp__year=year_now,
    #                                      created_timestamp__month__lte=month_now).select_related("category").annotate(month=TruncMonth('created_timestamp')).values('month').values("category", "month", 'amount', "id", "comment", "created_timestamp", "category__sub_categ__name").order_by('month')

    # # глобальные подкатегории по оперсчет
    sub_category_operation = SubCategoryOperation.objects.filter(
        meta_category="oper_account")

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

    operation_old_year = Operation.objects.filter(meta_categ='oper_account', created_timestamp__year__lt=year_now).annotate(year=TruncYear(
        "created_timestamp")).values('year').annotate(total_absolute_year=Sum('amount', default=0)).values('year', 'total_absolute_year')

    def old_operation(request):
        # operation_old_year2 = Operation.objects.filter(meta_categ='oper_account', created_timestamp__year__lt=year_now).annotate(year=TruncYear(
        #     "created_timestamp")).values('year').annotate(total_absolute_year=Sum('amount', default=0)).values('year', 'total_absolute_year')

        month_arr1 = []
        i = 0
        for m in months:
            i += 1
            month = {
                "name_month": m,
                "month": i,
            }
            month_arr1.append(month)

        month_arr1.reverse()

        dataset_old = []
        for year_arr_cat in range(len(operation_old_year)):

            year_olds = {
                "years": operation_old_year[year_arr_cat]['year'].year,
                "year": operation_old_year[year_arr_cat]['year'].year,
                "year_stamp": operation_old_year[year_arr_cat]['year'],
                "total_absolute_year": operation_old_year[year_arr_cat]['total_absolute_year'],
                "total_month_tag": 3,
                "month": None,
                "sub_categ_id": None,
                "total_year_in_categ": []
            }
            for cat in name_categ_list:
                categ = {
                    "years": operation_old_year[year_arr_cat]['year'].year,
                    "year": operation_old_year[year_arr_cat]['year'].year,
                    "category_operation_sub_categ": cat['category_operation_sub_categ'],
                    "category_operation_name": cat['category_operation_name'],
                    "category_operation_id": cat['category_operation_sub_categ_id'],
                    "total_month_tag": 4,
                    "total_month_categ": 0,
                }

                year_olds["total_year_in_categ"].append(categ)

            for v in name_sub_categ_list:
                months_act = {
                    "year": operation_old_year[year_arr_cat]['year'].year,
                    "total_month": 0,
                    "total_month_tag": 0,
                    "sub_categ": v['category_sub_categ'],
                    "sub_categ_id": v['category_sub_categ_id']
                }
                year_olds["total_year_in_categ"].append(months_act)

            year_old = {
                'year': operation_old_year[year_arr_cat]['year'].year,
                "item": []
                # year_arr_cat['year'].year: [],
            }

            year_old['item'].append(year_olds)

            for month_arr2 in range(1, 13):
                # для тоталов по субкатегориям мес
                for v in name_sub_categ_list:
                    months_act = {
                        "year": operation_old_year[year_arr_cat]['year'].year,
                        "month": month_arr2,
                        "month_name": months[month_arr2 - 1],
                        "total_month": 0,
                        "total_month_tag": 0,
                        "sub_categ": v['category_sub_categ'],
                        "sub_categ_id": v['category_sub_categ_id'],

                    }
                    year_old['item'].append(months_act)
                #  для каждого мес категорий месяцов
                for cat in name_categ_list:
                    category_operations = {
                        "year": operation_old_year[year_arr_cat]['year'].year,
                        "month": month_arr2,
                        "month_name": months[month_arr2 - 1],
                        "category_operation_sub_categ": cat['category_operation_sub_categ'],
                        "category_operation_name": cat['category_operation_name'],
                        "category_operation_id": cat['category_operation_sub_categ_id'],
                        "total_month_tag": 1,
                        "total_month_categ": 0,
                        "id_operation": '',
                        "comments": []


                    }

                    year_old['item'].append(category_operations)

            dataset_old.append(year_old)

        for data in dataset_old:
            year_data = data['year']
            for item in data['item']:
                for oper_old in operation_old:

                    if item['year'] == oper_old['created_timestamp'].year:
                        if item['month'] == oper_old['month'].month:

                            if item['total_month_tag'] == 0:
                                if item['sub_categ_id'] == oper_old['category__sub_categ__id']:
                                    item['total_month'] += oper_old['amount']

                            if item['total_month_tag'] == 1:
                                if item['category_operation_id'] == oper_old['category']:
                                    item['total_month_categ'] += oper_old['amount']
                                    # комментарии к операциям
                                    item['id_operation'] = item['id_operation'] + \
                                        str(oper_old['id']) + "-"
                                    if oper_old['comment']:
                                        comment = {
                                            "data": oper_old['created_timestamp'],
                                            "sum": oper_old['amount'],
                                            "comment": oper_old['comment'],

                                        }
                                        item['comments'].append(comment)

                        # годовые тоталы
                        if item['month'] == None:
                            for all_item in item["total_year_in_categ"]:
                                if all_item['total_month_tag'] == 4:
                                    if all_item['category_operation_id'] == oper_old['category']:
                                        all_item['total_month_categ'] += oper_old['amount']
                                elif all_item['total_month_tag'] == 0:
                                    if all_item['sub_categ_id'] == oper_old['category__sub_categ__id']:
                                        all_item['total_month'] += oper_old['amount']

        return dataset_old
    dataset_olds = old_operation(request)

    context = {
        'type_url': type_url,
        "category_operation": category_operation,
        "month_names": month_names,
        "dataset": dataset,
        "data": data,
        "year_now": year_now,
        "months": months,
        "operation_old_year": operation_old_year,
        "dataset_old": dataset_olds,



    }

    return render(request, "operation/operation_inside_oper_acount.html", context)


# налоги
def operation_inside_nalog(request):
    title = "34534534"

    context = {
        "title": title,
    }
    return render(request, "operation/operation_inside_nalog.html", context)


# зарплаты
def operation_inside_salary(request):
    title = "salary"
    type_url = 'operation_inside'
    # даты
    data = datetime.now()
    year_now = datetime.now().year
    month_now = datetime.now().month
    date_start_year = str(year_now)+"-01-01"

    # date_end__gte=date_start_year,

    def employee_cache():
        def cache_function():

            employee = Employee.objects.filter(
                Q(date_end__isnull=True) | Q(date_end__gte=date_start_year)).values("name", "last_name", 'id', "date_start", 'date_end')
            return employee
        return loc_mem_cache('employee', cache_function, 0)

    employee = employee_cache()

    def category_operation_cache():
        def cache_function():
            category_operation_salary = CategoryOperation.objects.filter(
                meta_categ='salary').select_related("sub_categ").values("sub_categ", "meta_categ", 'name', "sub_categ__name", 'id',)
            return category_operation_salary

        return loc_mem_cache('category_operation_salary', cache_function, 200)
    category_operation = category_operation_cache()

    operation = Operation.objects.filter(meta_categ='salary', created_timestamp__year=year_now,
                                         created_timestamp__month__lte=month_now).select_related("category").annotate(month=TruncMonth('created_timestamp')).values('month').values("category", "month", 'amount', "id", "comment", "created_timestamp", "category__sub_categ__name", "people").order_by('month')

    # актуальные месяца нынешнего года
    month_names = []
    for month in range(1, month_now+1):
        month_name = months[month - 1]

        month_names.append({
            "name_month": month_name,
            "month": month,
        })

    month_names.reverse()
    # глобальные подкатегории по ЗП
    sub_category_operation = SubCategoryOperation.objects.filter(
        meta_category="salary")
    name_sub_categ_list = []
    for name_sub_categ in sub_category_operation:
        name_sub_categ_list.append({
            "category_sub_categ": name_sub_categ.name,
            "category_sub_categ_id": name_sub_categ.id,
        })

    name_categ_list = []
    for name_categ in category_operation:
        name_categ_list.append({
            "category_operation_sub_categ": name_categ['sub_categ__name'],
            "category_operation_name": name_categ['name'],
            "category_operation_sub_categ_id": name_categ['id'],
            "category_operation_id": name_categ['sub_categ'],
        })
    employee_dataset = []
    total_employee = []
    for empl in employee:
        people = {
            "id": empl["id"],
            "item": []
        }
        people_old = {
            "id": empl["id"],

            "item": []
        }
        for mont in reversed(range(1, month_now+1)):

            for cat in name_categ_list:
                category_operations = {
                    "month": mont,
                    "month_name": months[mont - 1],
                    "category_operation_sub_categ": cat['category_operation_sub_categ'],
                    "category_operation_name": cat['category_operation_name'],
                    "category_operation_id": cat['category_operation_sub_categ_id'],
                    "total_month_tag": 1,
                    "comments": 1,
                    "id_operation": "",
                    "total": 0,
                    "year_now": year_now,
                    "absolute_total_month": 0,
                    "total_month": 0,
                    "people_id": empl["id"]
                }
                people['item'].append(category_operations)
            for v in name_sub_categ_list:
                months_act = {
                    "total_all_month": 0,
                    "month": mont,
                    "month_name": months[mont - 1],
                    "total_month": 0,
                    "total_month_tag": 0,
                    "sub_categ": v['category_sub_categ'],
                    "sub_categ_id": v['category_sub_categ_id'],
                    "people_id": empl["id"]
                }

                people_old['item'].append(months_act)
            total = {
                "total_all_month": 0,
                "month": mont,
                "month_name": months[mont - 1],
                "people_id": empl["id"],
                "sub_categ": 0,
            }

            people_old['item'].append(total)
        total_employee.append(people_old)
        employee_dataset.append(people)

    #    операции за актуальный год по месяцам
    for dataset in employee_dataset:
        for y in range(len(operation)):

            if operation[y]["people"] == dataset['id']:
                for x in range(len(dataset["item"])):
                    if dataset["item"][x]['people_id'] == operation[y]["people"]:
                        if dataset["item"][x]['month'] == operation[y]['month'].month and dataset["item"][x]['category_operation_id'] == operation[y]['category']:
                            dataset["item"][x]['total'] = operation[y]['amount']
                            dataset["item"][x]['year'] = operation[y]['created_timestamp'].year
                            dataset["item"][x]['id_operation'] = operation[y]['id']

    for dataset_old in total_employee:
        # dataset_old['ООО'] = 0
        # dataset_old['ЗП $'] = 0
        # dataset_old['КВ $'] = 0
        # dataset_old['КВ ип'] = 0
        # dataset_old['квартальная премия'] = 0
        # dataset_old['Долг'] = 0
        for y in range(len(operation)):
            if operation[y]["people"] == dataset_old['id']:
                for x in range(len(dataset_old["item"])):
                    if dataset_old["item"][x]['people_id'] == operation[y]["people"]:
                        # if dataset_old["item"][x]['month'] == operation[y]['month'].month:
                        if dataset_old["item"][x]['sub_categ'] == 0:
                            if operation[y]['category'] == 38:
                                i = operation[y]["month"].month
                                if dataset_old["item"][x]['month'] == i-1:
                                    dataset_old["item"][x]['total_all_month'] = dataset_old["item"][x]['total_all_month'] + \
                                        operation[y]['amount']
                            else:
                                if dataset_old["item"][x]['month'] == operation[y]['month'].month:
                                    dataset_old["item"][x]['total_all_month'] = dataset_old["item"][x]['total_all_month'] + \
                                        operation[y]['amount']

                        if dataset_old["item"][x]['sub_categ'] == operation[y]['category__sub_categ__name']:
                            if operation[y]['category'] == 38:
                                i = operation[y]["month"].month
                                if dataset_old["item"][x]['month'] == i-1:
                                    dataset_old["item"][x]['total_month'] = dataset_old["item"][x]['total_month'] + \
                                        operation[y]['amount']
                            else:
                                if dataset_old["item"][x]['month'] == operation[y]['month'].month:
                                    dataset_old["item"][x]['total_month'] = dataset_old["item"][x]['total_month'] + \
                                        operation[y]['amount']

            else:
                pass

    operation_old_year = Operation.objects.filter(meta_categ='salary', created_timestamp__year__lt=year_now).annotate(year=TruncYear(
        "created_timestamp")).values('year').annotate(total_absolute_year=Sum('amount', default=0)).values('year', 'total_absolute_year')

    def old_years_oper():
        operation_old = Operation.objects.filter(meta_categ='salary', created_timestamp__year__lt=year_now).select_related("category").annotate(month=TruncMonth(
            'created_timestamp')).values('month').values("category", "month", 'amount', "id", "comment", "created_timestamp", "category__sub_categ__name", "people").order_by('month')

        month_arr1 = []
        i = 0
        for m in months:
            i += 1
            month = {
                "name_month": m,
                "month": i,
            }
            month_arr1.append(month)

        month_arr1.reverse()
        employee_olds = []
        total_employee_olds = []
        for year_arr_cat in range(len(operation_old_year)):
            for empl in employee:
                people = {
                    "id": empl["id"],
                    "year": operation_old_year[year_arr_cat]['year'].year,
                    "item": []
                }
                people_old = {
                    "id": empl["id"],
                    "year": operation_old_year[year_arr_cat]['year'].year,
                    "item": []
                }
                for mont in range(1, 13):

                    for cat in name_categ_list:
                        category_operations = {
                            "year": operation_old_year[year_arr_cat]['year'].year,
                            "month": mont,
                            "month_name": months[mont - 1],
                            "category_operation_sub_categ": cat['category_operation_sub_categ'],
                            "category_operation_name": cat['category_operation_name'],
                            "category_operation_id": cat['category_operation_sub_categ_id'],
                            "total_month_tag": 1,
                            "comments": 1,
                            "id_operation": "",
                            "total": 0,
                            "absolute_total_month": 0,
                            "total_month": 0,
                            "people_id": empl["id"]
                        }
                        people['item'].append(category_operations)
                    for v in name_sub_categ_list:
                        months_act = {
                            "year": operation_old_year[year_arr_cat]['year'].year,
                            "total_all_month": 0,
                            "month": mont,
                            "month_name": months[mont - 1],
                            "total_month": 0,
                            "total_month_tag": 0,
                            "sub_categ": v['category_sub_categ'],
                            "sub_categ_id": v['category_sub_categ_id'],
                            "people_id": empl["id"]
                        }

                        people_old['item'].append(months_act)
                    total = {
                        "year": operation_old_year[year_arr_cat]['year'].year,
                        "total_all_month": 0,
                        "month": mont,
                        "month_name": months[mont - 1],
                        "people_id": empl["id"],
                        "sub_categ": 0,
                    }

                    people_old['item'].append(total)

                for cat in name_categ_list:
                    category_operations = {
                        "xxx": 999,
                        "year": operation_old_year[year_arr_cat]['year'].year,
                        "month": 0,
                        "month_name": 0,
                        "category_operation_sub_categ": cat['category_operation_sub_categ'],
                        "category_operation_name": cat['category_operation_name'],
                        "category_operation_id": cat['category_operation_sub_categ_id'],
                        "total_month_tag": 0,
                        "total": 0,
                        "absolute_total_month": 0,
                        "total_month": 0,
                        "people_id": empl["id"]
                    }
                    people['item'].append(category_operations)

                total_employee_olds.append(people_old)
                employee_olds.append(people)

        for dataset in employee_olds:
            for y in range(len(operation_old)):
                print(operation_old[y])
                if operation_old[y]["people"] == dataset['id']:

                    for x in range(len(dataset["item"])):

                        if dataset["item"][x]['people_id'] == operation_old[y]["people"]:
                            # if dataset["item"][x]['year'] == operation[y]['created_timestamp'].year:
                            if dataset["item"][x]['total_month_tag'] == 0:
                                if dataset["item"][x]['category_operation_id'] == operation_old[y]['category'] and dataset["item"][x]['year'] == operation_old[y]['created_timestamp'].year:
                                    dataset["item"][x]['absolute_total_month'] = dataset["item"][x]['absolute_total_month'] + \
                                        operation_old[y]['amount']

                                    dataset["item"][x]['id_operation'] = operation_old[y]['id']
                            elif dataset["item"][x]['total_month_tag'] == 1:
                                if dataset["item"][x]['month'] == operation_old[y]['month'].month and dataset["item"][x]['category_operation_id'] == operation_old[y]['category'] and dataset["item"][x]['year'] == operation_old[y]['created_timestamp'].year:
                                    dataset["item"][x]['total'] = operation_old[y]['amount']

                                    dataset["item"][x]['id_operation'] = operation_old[y]['id']

        return employee_olds

    old_operation = old_years_oper()

    context = {
        "title": title,
        "type_url": type_url,
        "employees": employee,
        "month_names": month_names,
        "data": data,
        "category_operation": category_operation,
        "dataset": employee_dataset,
        "total_employee": total_employee,
        "old_operation": old_operation,
        "operation_old_year": operation_old_year,
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
