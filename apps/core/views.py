from django.http import HttpResponse
from django.shortcuts import render

from apps.service.models import Adv


def index(request):
    title = "Главная"
    context = {
        "title": title,

    }

    return render(request, "core/index.html", context)

def tech(request):

    title = "Тех.раздел"
    
    category_adv = Adv.objects.all()
    
    context = {
        "title": title,
        "tech_adv_category":category_adv,

    }

    return render(request, "core/tech.html", context)

  