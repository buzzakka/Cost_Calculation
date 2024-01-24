from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('index/', TemplateView.as_view(template_name='index.html'), name='index')
]