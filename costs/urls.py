from django.urls import path, include

from .views import *

app_name = 'costs'

categories_urls = [
    path('add-category/', AddCategoryView.as_view(), name='add_category'),
    path('delete-category/<int:pk>/', CategoryDeleteView.as_view(), name='delete_category'),
]

urlpatterns = [
    path('main/', MainView.as_view(), name='main'),
    path('history/', CostsHistory.as_view(), name='history'),
    path('categories/', include(categories_urls)),
]
