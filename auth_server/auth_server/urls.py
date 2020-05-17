"""auth_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from auth_server import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('token', views.GenerateTokenView.as_view()),
    path('token/refresh/', views.RefreshTokenView.as_view()),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('authorize',views.AuthorizationView.as_view()),
    path('new-user',views.AddAccountView.as_view()),

    path('new-client',views.AddClientView.as_view())
]
