from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('view_blog/<str:uuid>/', views.view_blog, name='view_blog_post'),
    path('blogs/', views.all_blog_posts, name='view_all_blog_posts'),
]