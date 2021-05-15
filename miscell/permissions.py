from django.core.exceptions import ObjectDoesNotExist

import rest_framework.permissions as rest_permissions


class IsOwnerOrReadOnly(rest_permissions.BasePermission):
    '''
    This permission is used to allow modification of object
    only for it`s owner/creator.
    '''
    def has_object_permission(self, request, view, obj):
        if request.method in rest_permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user

class IsOwnerOrAssigned(rest_permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if hasattr(obj, 'assign'):
            try:
                _ = obj.assign.get(username=request.user.username)
                return True
            except ObjectDoesNotExists:
                return False
        
