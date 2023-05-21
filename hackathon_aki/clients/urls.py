from django.urls import path
from . import views

urlpatterns = [
    path('', views.registration, name='registration'),
    path('profile', views.show_client_profile, name='show_client_profile'),
]
