import django.utils.timezone as django_timezone

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.decorators import action


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.authtoken.views import ObtainAuthToken

from users.serializers import (
    UserSerializer,
    ProfileSerializer,
    PasswordSerializer,
    UserNameSerializer
)

from miscell import permissions

UserModel = get_user_model()

class ChangeUserApi(GenericViewSet):
    permission_classes = [
        IsAuthenticated,
        permissions.IsOwnerOrReadOnly
    ]

    @action(methods=['POST'], detail=False)
    def change_password(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        pwds = serializer(data=request.data)
        pwds.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(pwds.validated_data['old_password']):
            return Response(data={'error': 'incorrect password'},
                status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(pwds.validated_data['new_password'])
        user.save()
        return Response(status=status.HTTP_200_OK)
    
    @action(methods=['POST'], detail=False)
    def change_login(self, request):
        serializer = self.get_serializer_class()
        usr_name = serializer(data=request.data)
        if not usr_name.is_valid(raise_exception=False):
            return Response(data=usr_name.errors,
                status=status.HTTP_400_BAD_REQUEST)
        
        r_user = request.user.username
        r_user.username = serializer.validated_data['new_name']
        r_user.save()

        return Response(data={'warning': 'not implemented', 'nn': request.data},
            status=status.HTTP_501_NOT_IMPLEMENTED)
    
    def get_serializer_class(self):
        if self.action == 'change_password':
            return PasswordSerializer
        elif self.action == 'change_login':
            return UserNameSerializer


class UserListApiView(ReadOnlyModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]
    
    class Meta:
        fields = ['pk', 'username', 'first_name', 'last_name']


class ProfileView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        serialized = ProfileSerializer(user)
        return Response(serialized.data)


class RetrieveAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        user.last_login = django_timezone.now()
        user.save(update_fields=['last_login'])
        return Response({'token': token.key})
