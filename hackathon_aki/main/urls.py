from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('logout/', views.logout, name='logout'),
    path('reset_password/<str:verification_code>/', views.reset_password, name='reset_password'),
    path('email_verification/<str:verification_code>/', views.email_verification, name='email_verification'),
]
