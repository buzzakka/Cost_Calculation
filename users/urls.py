from django.contrib.auth.views import (PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView,
                                       PasswordChangeView, PasswordResetView)
from django.urls import path
from django.views.generic import TemplateView

from .views import *

app_name = 'users'

urlpatterns = [
    path('login/',
         UserLoginView.as_view(),
         name='login'
         ),
    path('logout/', logout_user, name='logout'),

    path('register/', UserRegisterView.as_view(), name='register'),

    path('password-change/',
         PasswordChangeView.as_view(
             template_name='users/change-password.html',
             extra_context={'title': "Изменить пароль"},
             success_url=reverse_lazy('users:index')
         ),
         name='change_password'
    ),

    path('password-reset/',
         PasswordResetView.as_view(
             template_name='users/password_reset_form.html',
             email_template_name='users/password_reset_email.html',
             success_url=reverse_lazy('users:password_reset_done')
         ),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html',
             success_url=reverse_lazy('users:password_reset_complete')
         ),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

    path('index/', TemplateView.as_view(template_name='index.html'), name='index')
]