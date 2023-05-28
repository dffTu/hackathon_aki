from django.urls import path
from . import views


urlpatterns = [
    path('', views.redirect_to_organizer_profile),
    path('profile/', views.show_organizer_profile, name='show_organizer_profile'),
    path('profile/schedule/', views.show_organizer_schedule, name='show_organizer_schedule'),
    path('profile/platforms/', views.redirect_to_first_page_of_organizer_platforms, name='redirect_to_first_page_of_organizer_platforms'),
    path('profile/platforms/<int:page_id>/', views.show_organizer_platforms, name='show_organizer_platforms'),
    path('profile/platforms/add/', views.create_platform, name='create_platform'),
    path('profile/platforms/<int:platform_id>/change/', views.change_platform, name='change_platform'),
    path('profile/delete_entry/<int:platform_id>/<int:day>/<int:month>/<int:year>/', views.delete_entry, name='delete_entry'),
    path('profile/delete_registration/<int:platform_id>/<int:client_id>/<int:day>/<int:month>/<int:year>/', views.delete_registration, name='delete_registration'),
    path('profile/add_entry/<int:platform_id>/<int:day>/<int:month>/<int:year>/', views.add_entry, name='add_entry'),
    path('profile/add_registration/<int:platform_id>/<int:day>/<int:month>/<int:year>/', views.add_registration, name='add_registration'),
    path('profile/change_price/<int:platform_id>/<int:day>/<int:month>/<int:year>/', views.change_price, name='change_price'),
]
