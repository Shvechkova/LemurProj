from django import forms

from apps.employee.models import Employee


class EmployeeNewForm(forms.ModelForm):
    class Meta:
        model = Employee
        # fields = ('client_name',)
        fields = "__all__"