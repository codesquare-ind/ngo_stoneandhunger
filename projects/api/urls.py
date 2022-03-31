from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('view_case/<str:uuid>/', views.view_case, name='view_case'),
    path('view_all_cases/', views.get_all_active_case, name='view_all_cases'),

    path('my_cases/', views.view_my_cases, name='view_my_cases'),
    path('my_donations/', views.view_my_donations, name='view_my_donations'),

    path('create_case/', views.create_case, name='create_case_api'),
    path('approve_case/<str:uuid>/', views.approve_case, name='approve_case'),
]