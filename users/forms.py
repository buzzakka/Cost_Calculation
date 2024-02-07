from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    """ Форма регистрации пользователя """

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ('username', 'email', 'password1', 'password2'):
            self.fields[fieldname].help_text = None

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')
