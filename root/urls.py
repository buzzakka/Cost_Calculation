from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('apps.costs.urls')),
    path('api/v1/', include('api_v1.urls')),
]
