from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    # path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('email_verification/<str:verification_code>/', views.email_verification, name='email_verification')
]
