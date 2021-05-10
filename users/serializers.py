from rest_framework.serializers import ModelSerializer

from users.models import CustomUser

class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('pk', 'username', 'first_name', 'last_name')

class ProfileSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'pk',
            'username',
            'first_name',
            'last_name',
            'last_login',
            'user_projects',
            'user_deals',
            'user_assigned_deals',
            'user_tasks',
            'user_assigned_tasks',
        )

