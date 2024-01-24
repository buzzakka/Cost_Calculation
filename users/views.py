from django.contrib.auth.views import LoginView
from .forms import *


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}
