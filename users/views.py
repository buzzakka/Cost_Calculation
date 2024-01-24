from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (PasswordResetCompleteView, PasswordChangeView, PasswordResetView, LoginView,
                                       PasswordResetDoneView)
from django.contrib.auth import logout
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .forms import *


class UnauthorizedOnlyMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('users:index'))
        return super().dispatch(request, *args, **kwargs)


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return reverse_lazy('users:index')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('users:login'))


class UserRegisterView(UnauthorizedOnlyMixin, CreateView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    extra_context = {'title': 'Регистрация'}

    def get_success_url(self) -> str:
        return reverse_lazy('users:index')


class UserChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    extra_context = {'title': 'Изменить пароль'}
    success_url = reverse_lazy('users:index')


class UserPasswordResetView(UnauthorizedOnlyMixin, PasswordResetView):
    template_name = 'users/password_reset_form.html'
    extra_context = {'title': 'Сброс пароля'}
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')


class UserPasswordResetCompleteView(UnauthorizedOnlyMixin, PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
    extra_context = {'title': 'Сброс пароля'}


class UserPasswordResetDoneView(UnauthorizedOnlyMixin, PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'
    extra_context = {'title': 'Сброс пароля'}
