from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter
from .views import *

router = SimpleRouter()
router.register(r'', CustomCategoriesAPIViewSet)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('common-categories/', StandartCategoriesAPIView.as_view()),
    path('custom-categories/', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
