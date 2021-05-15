from rest_framework.serializers import (ModelSerializer, 
                                        StringRelatedField,
                                        RelatedField)

import projects.models as projects_models


class UsersField(RelatedField):
    def get_queryset(self):
        super().get_queryset()

    def to_representation(self, value):
        return [usr.username for usr in value.all()]
    
    def to_internal_value(self, data):
        return data


class GenericForeignField(RelatedField):
    '''
    Generic foreign key for project/deal
    representation in task serializer
    '''
    def get_queryset(self):
        super().get_queryset()
        
    def to_representation(self, value):
        return str(value.model)

    def to_internal_value(self, data):
        pass


class TaskSerializer(ModelSerializer):
    created_by = StringRelatedField()
    assign = UsersField()
    content_type = GenericForeignField(required=False)
    class Meta:
        model = projects_models.TaskModel
        fields = '__all__'
        

class ProjectSerializer(ModelSerializer):
    created_by = StringRelatedField()

    class Meta:
        model = projects_models.Project
        fields = "__all__"


class DealSerializer(ModelSerializer):
    created_by = StringRelatedField()
    
    class Meta:
        model = projects_models.Deal
        fields = '__all__'
