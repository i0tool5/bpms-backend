from django.urls import re_path

from rest_framework.routers import DefaultRouter

import projects.views as views
import companies.views as c_views

router = DefaultRouter()
router.register(r"projects", views.ProjectApiView, basename='projects')
router.register(r"deals", views.DealApiView)
router.register(r'tasks', views.TaskApiView, basename='tasks')

urlpatterns = [
    # API Views
    re_path(
        r'^api/projects/delete-multiple/?$',
        views.MultipleProjectsDeleteApiView.as_view()
    ),
    re_path(r'^api/statuses/?$', views.StatusApiView.as_view(),
        name='statuses')
]
