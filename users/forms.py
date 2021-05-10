from django.contrib.auth.forms import UserCreationForm

from users.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

        labels = {
            'username': 'Имя пользоваетля',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'E-mail',
        }