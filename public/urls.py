from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('gallery', views.gallery, name='gallery'),

    path('terms_of_usage', views.terms, name='terms_of_usage'),
    path('privacy_policy', views.policy, name='privacy_policy'),
]
