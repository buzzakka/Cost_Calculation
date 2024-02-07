from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter
from .views import *

app_name = 'api_v1'

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]

router = SimpleRouter()
router.register(r'common_categories', StandartCategoriesAPIView, basename='common_categories')
router.register(r'custom-categories', CustomCategoriesAPIViewSet, basename='custom_categories')
router.register(r'costs', CostsAPIViewSet, basename='costs')
urlpatterns += router.urls
