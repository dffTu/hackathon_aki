from django.urls import path
from . import views


urlpatterns = [
    path('', views.redirect_to_organizer_profile, name='redirect_to_organizer_profile'),
    path('profile/', views.show_organizer_profile, name='show_organizer_profile'),
    path('registration/', views.registration, name='registration'),
]
