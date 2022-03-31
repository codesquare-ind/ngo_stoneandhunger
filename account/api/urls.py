from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


app_name = 'account'

urlpatterns = [
    path('register/', views.user_registration_view, name='register_api'),
    path('login/', obtain_auth_token, name='login_api'),
    path('change_password/', views.change_password, name='change_password'),

    path('complete_profile/', views.complete_profile, name='complete_profile'),
    path('get_profile/', views.get_profile, name='profile'),
]