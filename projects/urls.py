from django.urls import path, re_path

from .views import *


urlpatterns = [
    path('gallery/', ProjectsDetailView.as_view(), name='gallery'),
]