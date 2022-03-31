from django.urls import path
from . import views


urlpatterns = [
    path('events', views.events, name='events'),
    path('events/details/<str:pk>', views.event_details, name='event_details'),
    path('events/create', views.add_event, name='create_event'),
    path('events/edit/<str:pk>', views.edit_event, name='edit_event'),
    path('events/delete/<str:pk>', views.del_event, name='del_event'),

    path('become_volunteer', views.volunteer, name='volunteer'),
    path('form_submitted', views.volunteer_successful, name='v_successful'),
    path('vol_accepted/<str:pk>', views.volunteer_accept, name='v_accept'),
    path('vol_rejected/<str:pk>', views.volunteer_reject, name='v_reject'),

    path('vol_del/<str:pk>', views.vol_del, name='v_del'),
]