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
    '''
    PasswordSerializer is used in change user password process
    to serialize and validate old and new password sent by user
    '''
    old_password = serializers.CharField(allow_blank=False)
    new_password = serializers.CharField(allow_blank=False, min_length=10)

class UserNameSerializer(serializers.Serializer):
    '''
    UserNameSerializer used in change user's name process to
    to serialize and validate new nickname sent by user
    '''
    new_name = serializers.CharField(allow_blank=False, min_length=8)

    def validate(self, attrs):
        v_name = attrs['new_name']
        print('DEBUG:', attrs)
        usrs = CustomUser.objects.filter(username__iexact=v_name).count()
        if usrs > 0:
            raise serializers.ValidationError('user with given username already exists')

        return super().validate(attrs)
        
