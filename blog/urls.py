from django.urls import path
from . import views


urlpatterns = [
    path('blog', views.blog, name='blog'),
    path('blog/details/<str:uuid>', views.details, name='blog_post'),
    path('blog/create', views.create_blog, name='create_blog'),
    path('blog/edit/<str:uuid>', views.edit_blog, name='edit_blog'),
    path('blog/delete/<str:uuid>', views.delete_blog, name='del_blog'),


    path('edit_comment/<str:pk>', views.edit_comment, name='edit_comment'),
    path('delete_comment/<str:pk>', views.delete_comment, name='delete_comment'),
]