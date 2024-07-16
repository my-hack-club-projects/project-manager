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
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView

from . import views as views_common

favicon_view = RedirectView.as_view(url='/static/favicon.ico/', permanent=True)

urlpatterns = [
    re_path(r'^favicon\.ico$', favicon_view),

    path('admin/', admin.site.urls),
    path('api/', include('project_manager.api_urls')),
    path('api/products/', include('products.urls')),
    path('accounts/', include('accounts.urls')),
    path("stripe/", include("djstripe.urls", namespace="djstripe")),


    path('', views_common.home, name='home'),
    re_path(r'^projects/(?P<path>.*)/$', views_common.projects, name='projects'),
    re_path(r'^(?P<path>.*)/$', views_common.anyother, name='anyother'),
]
