from django.urls import path, include

from .views import *

app_name = 'costs'

categories_urls = [
    path('', CategoriesListView.as_view(), name='categories_list'),
    path('add-category/', AddCategoryView.as_view(), name='add_category'),
    path('delete-category/<int:pk>/', DeleteCategoryView.as_view(), name='delete_category'),
    path('update-category/<int:pk>/', UpdateCategoryView.as_view(), name='update_category'),
]

cost_urls = [
    path('', MainView.as_view(), name='main'),
    path('history/', CostsHistory.as_view(), name='history'),
    path('add-cost/', AddCostView.as_view(), name='add_cost'),
    path('update-cost/<int:pk>/', UpdateCostView.as_view(), name='update_cost'),
    path('delete-cost/<int:pk>/', DeleteCostView.as_view(), name='delete_cost'),
]

urlpatterns = [
    path('costs/', include(cost_urls)),
    path('categories/', include(categories_urls)),
]
