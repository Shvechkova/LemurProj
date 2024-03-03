# views.service





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

# old_month = now.month - 1
# if old_month == 0 :
#     old_month = 12
# year = now.year
# if old_month == 12 :
#     year = year - 1

# # date_need =

# print(old_month,year)

# total_sum_all_operation_entry = 0
# total_sum_operation_entry_bank1 = 0
# total_sum_operation_entry_bank2 = 0
# total_sum_operation_entry_bank3 = 0

# # for oper in operation:
# #     if oper['type_operation'] == "entry":
# #         total_sum_all_operation_entry += oper['amount']

# #         if oper['bank'] == 1:
# #             total_sum_operation_entry_bank1 += oper['amount']

# #         elif oper['bank']== 2:
# #             total_sum_operation_entry_bank2 += oper['amount']
# #         elif oper['bank'] == 3:
# #             total_sum_operation_entry_bank3 += oper['amount']

# total_sum_all_operation_out = 0
# total_sum_operation_out_bank1 = 0
# total_sum_operation_out_bank2 = 0
# total_sum_operation_out_bank3 = 0

# # for oper_out in operation:
# #     if oper_out.type_operation == "out":
# #         total_sum_all_operation_out += oper_out.amount

# #         if oper_out.bank.id == 1:
# #             total_sum_operation_out_bank1 += oper_out.amount

# #         elif oper_out.bank.id == 2:
# #             total_sum_operation_out_bank2 += oper_out.amount
# #         elif oper_out.bank.id == 3:
# #             total_sum_operation_out_bank3 += oper_out.amount

# # total_diff_operation_entry = (
# #     total_month_contract_sum - total_sum_all_operation_entry
# # )

# if slug == "ADV":
#     total_diff_operation_out = total_month_diff_sum - total_sum_all_operation_out
# else:
#     suborder_total_other = SubcontractMonth.objects.filter(
#         month_bill__service=category_service,
#         created_timestamp__year=now.year,
#         created_timestamp__month=now.month, other__isnull=False
#     ).aggregate(total_amount=Sum('amount', default=0))

#     total_diff_operation_out = suborder_total_other["total_amount"] - \
#         total_sum_all_operation_out

# total_oper = [
#     {
#         "total_sum_all_operation_entry": total_sum_all_operation_entry,
#         # "total_diff_operation_entry": total_diff_operation_entry,
#         "total_sum_operation_entry_bank1": total_sum_operation_entry_bank1,
#         "total_sum_operation_entry_bank2": total_sum_operation_entry_bank2,
#         "total_sum_operation_entry_bank3": total_sum_operation_entry_bank3,
#         "total_sum_all_operation_out": total_sum_all_operation_out,
#         # "total_diff_operation_out": total_diff_operation_out,
#         "total_sum_operation_out_bank1": total_sum_operation_out_bank1,
#         "total_sum_operation_out_bank2": total_sum_operation_out_bank2,
#         "total_sum_operation_out_bank3": total_sum_operation_out_bank3,
#     }
# ]





# servise html
