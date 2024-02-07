from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm


class AddPlaceholderFormMixin:
    """ Добавляет placeholder к полям """

    def add_placeholder(self):
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label


class UserRegisterForm(UserCreationForm, AddPlaceholderFormMixin):
    """ Форма регистрации пользователя """

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.add_placeholder()

        for fieldname in ('username', 'email', 'password1', 'password2'):
            self.fields[fieldname].help_text = None

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm, AddPlaceholderFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_placeholder()


class CustomPasswordResetForm(PasswordResetForm, AddPlaceholderFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_placeholder()
