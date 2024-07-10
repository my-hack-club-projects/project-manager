"""
URL configuration for backend project.

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
from django.urls import include, path

from rest_framework.authtoken.views import obtain_auth_token

from . import views as views_common
from . import auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('project_manager.api_urls')),
    path('auth/login/token', obtain_auth_token, name='obtain-auth-token'),
    path('auth/login/', auth_views.UserLoginAPIView.as_view(), name='user-login'),
    path('auth/logout/', auth_views.UserLogoutAPIView.as_view(), name='user-logout'),
    path('auth/user/', auth_views.UserProfileAPIView.as_view(), name='user-profile'),

    # path('', views_common.index, name='index'), # This only works for the home page.
    # add a catch-all path to handle all other paths
    path('', views_common.index, name='index'),
    path('<path>', views_common.index, name='index'),
]
