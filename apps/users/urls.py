from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import path, reverse_lazy

from .views import (UserLoginView, logout_user, UserRegisterView, UserChangePasswordView, UserPasswordResetView,
                    UserPasswordResetDoneView, UserPasswordResetCompleteView)

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),

    path('register/', UserRegisterView.as_view(), name='register'),

    path('change-password/', UserChangePasswordView.as_view(), name='change_password'),

    path('password-reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html',
             success_url=reverse_lazy('users:password_reset_complete')
         ),
         name='password_reset_confirm'),
    path('password-reset/complete/', UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
