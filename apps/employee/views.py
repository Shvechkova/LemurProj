from audioop import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from apps.employee.forms import EmployeeNewForm
from apps.employee.models import Employee


# Create your views here.


def employee(request):
    form = EmployeeNewForm()
    if request.method == "POST":
        form = EmployeeNewForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)
    else:
        form = EmployeeNewForm()

    workers = Employee.objects.all()
    title = "Сотрудники"
    context = {
        "title": title,
        "form": form,
        "workers": workers,
    }

    return render(request, "employee/index.html", context)


def worker(request, worker_id):
    worker = Employee.objects.filter(id=worker_id)
    title = worker_id
    context = {
        "title": title,
        "worker": worker,
    }

    return render(request, "employee/worker.html", context)
