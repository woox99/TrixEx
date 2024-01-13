# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('TrixEx', views.index),
    path('TrixEx/login', views.login),
    path('TrixEx/demo', views.demo),
    path('TrixEx/home', views.home),
    path('TrixEx/logout', views.logout),
    path('TrixEx/create', views.create),
    path('TrixEx/getAll', views.getAll),
    path('TrixEx/bookmark/<int:projectId>', views.bookmark),
    path('TrixEx/like/<int:projectId>', views.like),
]