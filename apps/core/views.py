from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    title = "Главная"
    context = {
        "title": title,

    }

    return render(request, "core/index.html", context)
