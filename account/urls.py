from django.urls import path
from . import views
from django.contrib.auth import views as auth_view


urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),

    path('complete_profile/', views.complete_profile, name='complete_profile'),
    path('change_password/', views.change_password, name='change_password'),


    path('u/profile/', views.profile, name='profile'),

    path('reset_password/', auth_view.PasswordResetView.as_view(
        template_name='account/pw_reset_mail.html'), name='password_reset'),
    path('reset_password_sent/', auth_view.PasswordResetDoneView.as_view(
        template_name='account/email_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(
        template_name='account/confirm_new_password.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_view.PasswordResetCompleteView.as_view(
        template_name='account/pw_reset_done.html'), name='password_reset_complete'),

    path('pw_change/', auth_view.PasswordChangeView.as_view(
            template_name='account/change_pw.html'), name='password_change'),
    path('pw_change_done/', auth_view.PasswordChangeDoneView.as_view(
            template_name='account/pw_reset_done.html'), name='password_change_done')
]