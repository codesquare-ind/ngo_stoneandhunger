from django.urls import path
from . import views


urlpatterns = [
    path('profile', views.profile, name='a_profile'),
    path('register', views.a_register, name='a_register'),
    path('dashboard', views.dashboard, name='a_dashboard'),
    path('all_cases', views.all_cases, name='a_cases'),
    path('donors', views.donors, name='a_donors'),
    path('users', views.users_list, name='a_users'),
    path('subadmin/<str:pk>', views.add_subadmin, name='a_add_sub'),
    path('rem_subadmin/<str:pk>', views.rem_subadmin, name='a_rem_sub'),
    path('cases/<str:uuid>', views.case_details, name='a_case_details'),

    path('blog', views.blog, name='a_blog'),
    path('events', views.events, name='a_events'),
    path('media', views.media, name='a_media'),
    path('volunteer/', views.volunteer, name='a_volunteer'),

    path('gallery', views.gallery, name='a_gallery'),
    path('gallery/del/<str:pk>', views.del_img_set, name='a_gallery_del'),
    path('gallery/add/<str:pk>', views.add_new_images, name='a_new_img'),
    path('gallery/del/img/<str:pk>', views.del_img, name='a_del_img'),

    path('add_case', views.add_case, name='a_add'),
    path('edit_case/<str:uuid>', views.edit_case, name='a_edit'),
    path('approve_case/<str:uuid>', views.approve_case, name='a_approve'),
    path('reject_case/<str:uuid>', views.reject_case, name='a_reject'),
    path('delete_case/<str:uuid>', views.delete_case, name='a_delete'),
    path('close_case/<str:uuid>', views.close_case, name='a_close'),
]