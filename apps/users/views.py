from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (PasswordResetCompleteView, PasswordChangeView, PasswordResetView, LoginView,
                                       PasswordResetDoneView)
from django.contrib.auth import logout
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .forms import UserRegisterForm, CustomAuthenticationForm, CustomPasswordResetForm, CustomChangePasswordForm


class UnauthorizedOnlyMixin(View):
    """ Миксин для доступа к странице только неавторизованных пользователей """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('costs:main'))
        return super().dispatch(request, *args, **kwargs)


class UserLoginView(LoginView):
    """ Аутентификация пользователя """
    template_name = 'users/login.html'
    form_class = CustomAuthenticationForm
    extra_context = {'title': 'Авторизация'}
    redirect_authenticated_user = True


def logout_user(request):
    """ Логаут пользователя """
    logout(request)
    return HttpResponseRedirect(reverse_lazy('users:login'))


class UserRegisterView(UnauthorizedOnlyMixin, CreateView):
    """ Регистрация пользователя """
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')


class UserChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    """ Смена пароля """
    template_name = 'users/change_password.html'
    form_class = CustomChangePasswordForm
    extra_context = {'title': 'Изменить пароль'}
    success_url = reverse_lazy('users:index')


class UserPasswordResetView(UnauthorizedOnlyMixin, PasswordResetView):
    """ Сброс пароля """
    template_name = 'users/password_reset_form.html'
    form_class = CustomPasswordResetForm
    extra_context = {'title': 'Сброс пароля'}
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')


class UserPasswordResetCompleteView(UnauthorizedOnlyMixin, PasswordResetCompleteView):
    """ Сброс пароля успешен """
    template_name = 'users/password_reset_complete.html'
    extra_context = {'title': 'Сброс пароля'}


class UserPasswordResetDoneView(UnauthorizedOnlyMixin, PasswordResetDoneView):
    """ Сброс пароля подтвержден """
    template_name = 'users/password_reset_done.html'
    extra_context = {'title': 'Сброс пароля'}
