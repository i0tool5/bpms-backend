from django.db import router
from django.urls import include, re_path

from rest_framework.routers import DefaultRouter


from users.views import (
    UserListApiView,
    ProfileView,
    RetrieveAuthToken
)

router = DefaultRouter()
router.register(r'users', UserListApiView)

urlpatterns = [
    re_path(r'^api/login/?$', RetrieveAuthToken.as_view(), name="authtoken"),
    re_path(r'^api/users/profile/?$', ProfileView.as_view(), name="profile"),
]
