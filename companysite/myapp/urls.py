"""
URL configuration for newcompanypro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .views import CustomLoginView



urlpatterns = [

    path('admin/', admin.site.urls),
    path('', views.home, name='index'),
    path('home/', views.home, name='home'),
    path('search/', views.post_search, name='post_search'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('add_post/', views.add_post, name='add_post'),
    path('add_post_type/', views.add_post_type, name='add_post_type'),
    path('add_project/', views.add_project, name='add_project'),
    path('login/', CustomLoginView.as_view(), name='login_view'),
    path('register/', views.register_user, name='register'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),  # Redirect to home after logout

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
