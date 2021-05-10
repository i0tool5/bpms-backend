import django.utils.timezone as django_timezone

from django.contrib.auth.password_validation import validate_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.authtoken.views import ObtainAuthToken

from users.forms import CustomUserCreationForm
from users.models import CustomUser
from users.serializers import (
                    UserSerializer,
                    ProfileSerializer
                    )

from bpms import rest_permissions

class ChangePasswordApi(APIView):
    permission_classes = [
        IsAuthenticated,
        rest_permissions.IsOwnerOrReadOnly
    ]
    def put(self, request, *args, **kwargs):
        user = requset.user
        return Response()


class UserListApiView(ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
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
        token, created = Token.objects.get_or_create(user=user)
        user.last_login = django_timezone.now()
        user.save(update_fields=['last_login'])
        return Response({'token': token.key})
