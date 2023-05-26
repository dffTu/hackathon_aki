from django.urls import path
from . import views


urlpatterns = [
    path('', views.redirect_to_first_page, name='catalogue_unverified'),
]
