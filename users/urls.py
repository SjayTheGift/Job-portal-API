
from django.contrib import admin
from django.urls import path, include

from .views import (
    LogInView, 
    LogoutView, 
    DeveloperProfileView, 
    DeveloperProfileDetailView,
    DeveloperSignUpView,
    ClientSignUpView
    )

urlpatterns = [
    path('api/login/', LogInView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/signup/developer/', DeveloperSignUpView.as_view(), name='signup_developer'),
    path('api/signup/client/', ClientSignUpView.as_view(), name='signup_client'),

    path('api/developers/', DeveloperProfileView.as_view(), name='developers-list'),
    path('api/developers/<int:pk>/', DeveloperProfileDetailView.as_view(), name='developer-detail'),
]
