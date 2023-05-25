from django.urls import path
from . import views


urlpatterns = [
    path('', views.redirect_to_first_page),
    path('page/<int:page_id>/', views.show_page, name='show_page'),
    path('platform/<int:platform_id>/', views.show_platform_description, name='show_platform_description'),
    path('platform/<int:platform_id>/leave_comment', views.leave_comment, name='leave_comment'),
]
