import datetime
from apps.service.models import ServicesMonthlyBill, SubcontractMonth
from project.celery import app

@app.task
def creat_new_bill_month():
  print(123)
    
    # now = datetime.datetime.now()

    # old_month = now.month - 1
    # if old_month == 0:
    #     old_month = 12
    # year = now.year
    # if old_month == 12:
    #     year = year - 1

    # bill_now_old = ServicesMonthlyBill.objects.filter(
    #     created_timestamp__year=year, created_timestamp__month=old_month)

    # for old_bill in bill_now_old:
    #     subcontr_old = SubcontractMonth.objects.filter(month_bill=old_bill.id)

    #     new_bill = old_bill
    #     new_bill.pk = None
    #     old_bill_name = old_bill.contract_number
    #     new_bill.chekin_sum_entrees = False
    #     new_bill.chekin_sum_adv = False
    #     # name_bill = old_bill_name.split('/')
    #     # print(name_bill[0])
    #     new_name_bill = old_bill.service.name + \
    #         "/" + str(now.year)+"-" + str(now.month)
    #     new_bill.contract_number = new_name_bill

    #     new_bill.save()
    #     if subcontr_old.exists():
    #         for subs_old in subcontr_old:

    #             new_subs = subs_old
    #             new_subs.pk = None
    #             new_subs.month_bill_id = new_bill.id

    #             new_subs.save()
    #             new_bill_qurery = ServicesMonthlyBill.objects.filter(
    #                 id=new_bill.id).update(chekin_add_subcontr=True)
    #             # new_bill.update(chekin_add_subcontr=True)

    