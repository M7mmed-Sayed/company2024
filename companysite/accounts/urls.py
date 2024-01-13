# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(authentication_form=CustomAuthenticationForm), name='loginAc'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Add other authentication-related views as needed
]
