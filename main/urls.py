from django.urls import path, include
from django.contrib import admin
from django.conf.urls import url
from . import views

urlpatterns = [
    path('get-user-profile/<slug:pk>/', view=views.getUserProfile, name='get-user-profile' ),
    path('get-user/<slug:pk>/', view=views.getUser, name='get-user'),
    path('profile-images/', views.profileImages, name='profile-images'),
    path('update-user-profile/<slug:pk>/', view= views.updateUserProfile, name='update-user-profile'),
    path('get-coupon-amount/<uuid:code>/', view=views.getCouponAmount, name='get-coupon-amount'),
]
