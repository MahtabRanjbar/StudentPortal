"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from dashboard import views as dash_views
from django.contrib import admin
from django.contrib.auth import views as auth_Views
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),
    path("register", dash_views.register_view, name="register"),
    path("sign_in", auth_Views.LoginView.as_view(
        template_name='dashboard/login.html'), name="sign_in"),
    path("sign_out", auth_Views.LogoutView.as_view(
        template_name='dashboard/logout.html'), name="sign_out"),
    path("profile", dash_views.profile_view, name="profile"),
    
    
]
