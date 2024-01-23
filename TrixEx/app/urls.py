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
    path('TrixEx.com/view/<int:projectId>', views.view),
    path('TrixEx.com/edit/<int:projectId>', views.edit),
    path('TrixEx.com/search/', views.search),
    path('TrixEx.com/logout', views.logout),
    path('TrixEx.com/update/motto', views.updateMotto),
    path('TrixEx.com/comment/<int:projectId>', views.comment),
    path('TrixEx.com/reply/<int:commentId>', views.reply),
    path('TrixEx.com/delete/project/<int:projectId>', views.deleteProject),
    path('TrixEx.com/delete/comment/<int:commentId>', views.deleteComment),
    path('TrixEx.com/delete/reply/<int:replyId>', views.deleteReply),
    path('TrixEx/getAll', views.getAll), #AJAX
    path('TrixEx/getAllLanding', views.getAllLanding), #AJAX
    path('TrixEx/getAllByUser/<int:userId>', views.getAllByUser), #AJAX
    path('TrixEx/getBookmarks', views.getBookmarks), #AJAX
    path('TrixEx/search/projects/<str:searchKey>', views.getSearchProjects), #AJAX
    path('TrixEx/bookmark/<int:projectId>', views.bookmark), #AJAX
    path('TrixEx/like/project/<int:projectId>', views.likeProject), #AJAX
    path('TrixEx/like/comment/<int:commentId>', views.likeComment), #AJAX
    path('TrixEx/follow/<int:followeeId>', views.follow), #AJAX
    path('TrixEx/visibility/<int:projectId>', views.visibility), #AJAX
]