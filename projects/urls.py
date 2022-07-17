from django.urls import path
from . import views


urlpatterns = [
    path('u/dashboard', views.dashboard, name='u_dashboard'),
    path('u/cases', views.my_cases, name='my_cases'),
    path('u/donations', views.my_donations, name='my_donations'),
    path('u/cases/create', views.create_new_case, name='create_case'),

    path('all_cases', views.all_cases, name='all_cases'),
    path('case_details/<str:uuid>', views.case_details, name='case_details'),

    path('checkout/<str:id>', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
    path('failure/', views.failure, name='failure'),
    #path('pdf_test/', views.pdf_test_w, name='pdf_test'),
]
