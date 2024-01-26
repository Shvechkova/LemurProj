from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    title = "Главная"
    context = {
        "title": title,
        # 'content': "Магазин мебели HOME",
    }

    return render(request, "core/index.html", context)
