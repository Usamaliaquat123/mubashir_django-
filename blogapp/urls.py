from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.blog_list,name='blog_list'), #blog list
    path('post_comment', views.blog_post_comment, name='blog_post_comment'), #post comment
    path('comments/<int:pk>', views.blog_comments, name='blog_comments'), #blog comments
    path('<str:slug>', views.blog_view, name='blog_view'), #blog view
]