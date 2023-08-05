from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', ElectricHomeDetailView.as_view(), name='home'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('services/', services, name='services'),
    path('prices/', prices, name='prices'),
]