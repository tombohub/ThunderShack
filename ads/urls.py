from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='ads-home'),
    path('create-ad/', views.create_ad, name='create-ad'),
    path('ad/<int:pk>/delete/', views.delete, name='ads-delete'),
    path('ad/<int:pk>/edit/', views.edit, name='ads-edit'),
    path('ad/<int:pk>/<slug:slug>/', views.ad_details, name='ad-details'),
    path('myads/', views.user_ads, name='user-ads')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
