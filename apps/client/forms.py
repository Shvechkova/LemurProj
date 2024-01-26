from django import forms
from .models import Client, Contract
from apps.service.models import ServiceClient


class ClientNew(forms.ModelForm):
    class Meta:
        model = Client
        # fields = ('client_name',)
        fields = "__all__"
        



class NewServiceClient(forms.ModelForm):
    class Meta:
        model = ServiceClient
        fields = ["services_name", "client"]


class AddContract(forms.ModelForm):
    contract_number = forms.CharField()
    contract_sum = forms.IntegerField()
    date_start = forms.DateField()
    date_end = forms.DateField()

    class Meta:
        model = Contract
        fields = "__all__"


# class AddSubPeople(forms.ModelForm):
#     seosub_people = forms.CharField()
#     seosub_sum = forms.IntegerField()

#     class Meta:
#         model = SubcontractAll
#         fields = ["seosub_people", "seosub_sum"]


# class EmployeeDevNew(forms.ModelForm):
#     drvsub_people = forms.CharField()
#     drvsub_sum = forms.IntegerField()

#     # designersub_people = forms.CharField()
#     # designersub_sum = forms.IntegerField()

#     class Meta:
#         model = SubcontractAll
#         fields = ["drvsub_people", "drvsub_sum"]


# class EmployeeDesignNew(forms.ModelForm):
#     designersub_people = forms.CharField()
#     designersub_sum = forms.IntegerField()

#     class Meta:
#         model = SubcontractAll
#         fields = ["designersub_people", "designersub_sum"]


# class AddAdvService(forms.ModelForm):
#     class Meta:
#         model = SubcontractADV
#         fields = ["adv_name", "service_client"]


class UpdServiceClient(forms.ModelForm):
    id_service = forms.IntegerField()

    class Meta:
        model = ServiceClient
        fields =  ("__all__")
