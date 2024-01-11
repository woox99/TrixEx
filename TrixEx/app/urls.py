from django.urls import path
from . import views

urlpatterns = [
    path('TrixEx', views.index),
    path('TrixEx/login', views.login),
]