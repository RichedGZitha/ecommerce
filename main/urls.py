from django.urls import path, include
from django.contrib import admin
from django.conf.urls import url
from . import views

urlpatterns = [
    path('get-user-profile/<slug:pk>/', view=views.getUserProfile, name='get-user-profile' ),
    path('get-my-profile/', view=views.getMyProfile, name='get-my-profile'),
    path('get-user/<slug:pk>/', view=views.getUser, name='get-user'),
    path('profile-images/', views.profileImages, name='profile-images'),
    path('update-user-profile/<slug:pk>/', view= views.updateUserProfile, name='update-user-profile'),
    path('get-coupon-amount/<uuid:code>/', view=views.getCouponAmount, name='get-coupon-amount'),
    #path('get-csrf-token/', view=views.getCSRFTokenView, name = 'get-csrf-token'),
    path('activate/<str:uid>/<str:token>/', view=views.activateUser, name='activation-confirmation'),
    path('email/reset/confirm/<str:uid>/<str:token>/', view=views.passwordReestConfirm, name='password-reest-confirm'),
    path('password-reset-successful/', view=views.passwordResetSuccessful, name = 'password-reset-successful'),
    
    path('logout/', view=views.LogoutView, name="logout"),
    path('logout-all/', view=views.LogoutAllView, name="logout-all"),
]
