from django import forms

from apps.operation.models import OperationEntry

class OperationEntryForm(forms.Form):
       
    bank = forms.CharField()
    amount = forms.IntegerField()
    id_contract = forms.IntegerField()
    # class Meta:
    #     model = OperationEntry
    #     fields = ('__all__')