"""iccs_crm_v2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from users.urls import router as users_router
from projects.urls import router as proj_router 
from companies.urls import router as comp_router

# Waste of memory, because all apps
# are using DefaultRouter class
main_router = DefaultRouter()
main_router.registry.extend(proj_router.registry)
main_router.registry.extend(users_router.registry)
main_router.registry.extend(comp_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('projects.urls')),
    path('', include('users.urls')),
    path(r'api/', include(main_router.urls)),
]
