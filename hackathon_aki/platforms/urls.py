from django.urls import path
from . import views


urlpatterns = [
    path('', views.redirect_to_first_page),
    path('page/<int:page_id>/', views.show_page, name='show_page'),
    path('platform/<int:platform_id>/', views.show_platform_description, name='show_platform_description'),
    path('platform/<int:platform_id>/delete', views.delete_platform, name='delete_platform'),
    path('platform/<int:platform_id>/verify', views.verify_platform, name='verify_platform'),
    path('platform/<int:platform_id>/unverify', views.unverify_platform, name='unverify_platform'),
    path('platform/<int:platform_id>/download_agreement', views.download_agreement, name='download_agreement'),
]
