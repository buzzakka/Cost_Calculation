from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    """ Форма регистрации пользователя """
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')
