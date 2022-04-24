from django.shortcuts import render
from django.views import View


# Create your views here.


# class Index(View):
#     template_name = "chatrooms/index.html"

def index(request):
    return render(request,"chatrooms/index.html")