from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .serializer import *
from .filters import *


class CategoriesAPIView(generics.ListAPIView):
    """
        Предоставляет список категорий пользователя + стандартные категории
    """
    queryset = CostCategory.objects.filter()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = (IsOwnerFilterBackend, DjangoFilterBackend)
    filterset_fields = ('id', 'name', 'is_custom')

