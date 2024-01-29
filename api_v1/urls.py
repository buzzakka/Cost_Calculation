from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter
from .views import *

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('common-categories/', StandartCategoriesAPIView.as_view()),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]

router = SimpleRouter()
router.register(r'custom-categories', CustomCategoriesAPIViewSet)
router.register(r'costs', CostsAPIViewSet)
urlpatterns += router.urls
