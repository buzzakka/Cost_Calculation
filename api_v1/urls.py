from django.urls import path, include
from .views import *


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('standart-categories/', StandartCategoriesAPIView.as_view()),
]
