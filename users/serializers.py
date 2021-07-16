from rest_framework import serializers 
from users.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('pk', 'username', 'first_name', 'last_name')

class ProfileSerializer(serializers.ModelSerializer):

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

class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(allow_blank=False)
    new_password = serializers.CharField(allow_blank=False, min_length=10)
