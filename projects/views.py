from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

from rest_framework.response import Response
from rest_framework import status, views, viewsets
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

import projects.models as proj_models
from miscell.permissions import (
    IsOwnerOrReadOnly,
    IsOwnerOrAssigned
)
from projects.serializers import (
    ProjectSerializer,
    DealSerializer, 
    TaskSerializer,
    StatusSerializer,
)


class ProjectsApiView(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly
    ]

    def get_queryset(self):
        return proj_models.Project.objects.filter(
            Q(public=True) | Q(created_by=self.request.user)
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        tasks = serializer.initial_data.pop('tasks', None)
        serializer.is_valid(raise_exception=True)
        proj = serializer.save(created_by=request.user)
        if tasks:
            for task in tasks:
                serial = TaskSerializer(data=task)
                serial.initial_data['object_id'] = proj.uid
                serial.is_valid(raise_exception=True)
                serial.validated_data['created_by'] = request.user
                serial.save(content_object=proj)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MultipleProjectsDestroyApiView(views.APIView):
    queryset = proj_models.Project.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    
    def delete(self, request, *args, **kwargs):
        objs = self.queryset.filter(pk__in=request.data["projects"])
        objs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DealsApiView(viewsets.ModelViewSet):
    queryset = proj_models.Deal.objects.all()
    serializer_class = DealSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TasksApiView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAssigned]

    def get_queryset(self):
        return proj_models.TaskModel.objects.filter(
            assign=self.request.user
        )

    def create(self, request, *args, **kwargs):
        cont_type = request.data.pop("content_type", None)
        identifier = request.data.get("object_id", None)
        cont_object = None
        content_type = None
        if cont_type == "projects":
            cont_object = proj_models.Project.objects.get(uid=identifier)
            content_type = ContentType(app_label="projects", model="project")
        elif cont_type == "deals":
            cont_object = proj_models.Deal.objects.get(uid=identifier)
            content_type = ContentType(app_label="projects", model="deal")

        serializer = self.serializer_class(data=request.data)
        dat = {
            'content_type': content_type,
            'content_object': cont_object,
            'object_id': identifier,
        }

        serializer.is_valid(raise_exception=True)
        serializer.validated_data.update(dat)
        serializer.save(created_by=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class StatusesApiView(ListCreateAPIView):
    queryset = proj_models.Status.objects.all()
    serializer_class = StatusSerializer
