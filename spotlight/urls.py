from django.urls import path
from . import views


urlpatterns = [
    path('media', views.media, name='media'),
    path('media/create', views.add_media, name='add_media'),
    path('media/delete/<str:pk>', views.del_img_set, name='del_media'),
    path('media/del/img/<str:pk>', views.del_img, name='del_img_media'),
    path('media/add/img/<str:pk>', views.add_new_images, name='add_img_media'),
]
