# # from django.shortcuts import render
# from django.http import HttpResponse
# from django.shortcuts import render
# from apps.service.models import ServiceClient 
# from apps.client.models import Client, Contract

# # Create your views here.

# def index(request):
#     latest_question_list = Client.objects.order_by("-id")
#     context = {"latest_question_list": latest_question_list}
#     return render(request, "/index.html", context)

# # def detail(request, client_name):
# #     return HttpResponse(client_name)