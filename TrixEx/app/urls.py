# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('TrixEx', views.index),
    path('TrixEx/login', views.login),
    path('TrixEx/demo', views.demo),
    path('TrixEx/home', views.home),
    path('TrixEx/bookmarks', views.bookmarks),
    path('TrixEx/create', views.create),
    # path('TrixEx/view/<int:project_id>', views.view),
    path('TrixEx/logout', views.logout),
    path('TrixEx/getAll', views.getAll),
    path('TrixEx/getBookmarks', views.getBookmarks),
    path('TrixEx/bookmark/<int:projectId>', views.bookmark),
    path('TrixEx/like/<int:projectId>', views.like),
]