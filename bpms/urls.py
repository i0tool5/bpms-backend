"""bpms URL Configuration"""

from django.urls import path, include, re_path

from rest_framework.routers import DefaultRouter

from users.urls import router as users_router
from projects.urls import router as proj_router 
from companies.urls import router as comp_router
from miscell.views import handle404

# Waste of memory, because all apps
# are using DefaultRouter class
main_router = DefaultRouter()
main_router.registry.extend(proj_router.registry)
main_router.registry.extend(users_router.registry)
main_router.registry.extend(comp_router.registry)

urlpatterns = [
    path('', include('projects.urls')),
    path('', include('users.urls')),
    path(r'api/', include(main_router.urls)),
    re_path(r'^api/.*/?$', handle404)
]
