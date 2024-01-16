# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('TrixEx.com', views.index),
    path('TrixEx.com/login', views.login),
    path('TrixEx.com/demo', views.demo),
    path('TrixEx.com/home', views.home),
    path('TrixEx.com/bookmarks', views.bookmarks),
    path('TrixEx.com/folder<int:folder_userId>/<str:username>', views.folder),
    path('TrixEx.com/create', views.create),
    path('TrixEx.com/view/<int:project_id>', views.view),
    path('TrixEx.com/logout', views.logout),
    path('TrixEx/getAll', views.getAll), #AJAX
    path('TrixEx/getAllLanding', views.getAllLanding), #AJAX
    path('TrixEx/getAllByUser/<int:userId>', views.getAllByUser), #AJAX
    path('TrixEx/getBookmarks', views.getBookmarks), #AJAX
    path('TrixEx/bookmark/<int:projectId>', views.bookmark), #AJAX
    path('TrixEx/like/<int:projectId>', views.like), #AJAX
    path('TrixEx/follow/<int:followeeId>', views.follow), #AJAX
]