from django.db import router
from django.urls import include, re_path
from django.views.generic import base

from rest_framework.routers import DefaultRouter


from users.views import (
    ChangeUserApi,
    UserListApiView,
    ProfileView,
    RetrieveAuthToken
)

router = DefaultRouter()
router.register(r'users', UserListApiView)
router.register(r'users/profile', ChangeUserApi, basename='user-config')

urlpatterns = [
    re_path(r'^api/login/?$', RetrieveAuthToken.as_view(), name="authtoken"),
    re_path(r'^api/users/profile/?$', ProfileView.as_view(), name="profile"),
]
