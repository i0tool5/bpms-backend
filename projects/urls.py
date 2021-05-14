from django.urls import re_path
from django.urls.conf import include

from rest_framework.routers import DefaultRouter

import projects.views as views
import users.views as u_views
import companies.views as c_views

router = DefaultRouter()
router.register(r"projects", views.ProjectApiView, basename='projects')
router.register(r"deals", views.DealApiView)
router.register(r'tasks', views.TaskApiView, basename='tasks')
router.register(r'users', u_views.UserListApiView)
router.register(r'companies', c_views.CompanyApiView)
router.register(r'contacts', c_views.ContactApiView)

urlpatterns = [
    # index
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    # API Views
    re_path(
        r'^api/projects/delete-multiple/?$',
        views.MultipleProjectsDeleteApiView.as_view()
    ),
    # API Views included from drf router
    re_path(r"api/", include(router.urls)),
]
