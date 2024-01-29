from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import *


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('standart-categories/', CategoriesAPIView.as_view()),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
