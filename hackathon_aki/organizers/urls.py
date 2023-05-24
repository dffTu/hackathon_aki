from django.urls import path
from . import views


urlpatterns = [
    path('', views.redirect_to_organizer_profile),
    path('profile/', views.show_organizer_profile, name='show_organizer_profile'),
    path('profile/platforms/', views.show_organizer_platforms, name='show_organizer_platforms'),
    path('profile/platforms/add', views.create_platform, name='create_platform'),
    # path('registration/', views.registration, name='organizer_registration'),
]
