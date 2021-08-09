from django.urls import re_path

from rest_framework.routers import DefaultRouter

import projects.views as views
import companies.views as c_views

router = DefaultRouter()
router.register(r"projects", views.ProjectsApiView, basename='projects')
router.register(r"deals", views.DealsApiView)
router.register(r'tasks', views.TasksApiView, basename='tasks')

urlpatterns = [
    # API Views
    re_path(
        r'^api/projects/delete-multiple/?$',
        views.MultipleProjectsDestroyApiView.as_view()
    ),
    re_path(r'^api/statuses/?$', views.StatusesApiView.as_view(),
        name='statuses')
]
