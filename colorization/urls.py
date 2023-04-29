from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='colorization_upload_file'),
]