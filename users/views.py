from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import *


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}
    redirect_authenticated_user = True


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('users:login'))
