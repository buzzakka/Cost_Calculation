from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .serializer import *
from .filters import *


class StandartCategoriesAPIView(generics.ListAPIView):
    """
        Предоставляет список стандартных (общих) категорий
    """
    queryset = CostCategory.objects.filter(is_custom=False)
    serializer_class = CategoriesSerializer
    permission_classes = (IsAuthenticated, )
    filterset_fields = ('id', 'name')


class CustomCategoriesAPIViewSet(ModelViewSet):
    """
        Предоставляет список категорий пользователя
    """
    queryset = CostCategory.objects.filter(is_custom=True)
    serializer_class = CategoriesSerializer
    filter_backends = (IsOwnerFilterBackend, DjangoFilterBackend)
    filterset_fields = ('id', 'name')

    def perform_create(self, serializer):
        # Устанавливаем текущего пользователя в поле "user" модели CostCategory
        serializer.save(user=self.request.user)


class CostsAPIViewSet(ModelViewSet):
    """
        Предоставляет список затра пользователя с подробной информацией
    """
    queryset = Cost.objects.order_by('-date')
    serializer_class = CostsSerializer
    filter_backends = (IsOwnerFilterBackend, DjangoFilterBackend)
    filterset_fields = ('id', 'value', 'category__id', 'category__name', 'description')

    def perform_create(self, serializer):
        # Устанавливаем текущего пользователя в поле "user" модели Cost
        serializer.save(user=self.request.user)
