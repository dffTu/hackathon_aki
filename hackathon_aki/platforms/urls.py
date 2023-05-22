from django.urls import path
from . import views


urlpatterns = [
    path('', views.redirect_to_first_page),
    path('page/<int:page_id>/', views.show_page, name='show_page'),
    path('create_platform/', views.create_platform, name='create_platform'),
]
