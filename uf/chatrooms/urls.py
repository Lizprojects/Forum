from django import views
from django.urls import path
from .views import index

app_name = "chatrooms"

urlpatterns = [path("", index, name="index")]
