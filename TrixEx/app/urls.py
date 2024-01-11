# app/urls.py
from django.urls import path
from .views import user

urlpatterns = [
    path('TrixEx', user.index),
    path('TrixEx/login', user.login),
    path('TrixEx/demo', user.demo),
    path('TrixEx/home', user.home),
]