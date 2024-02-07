from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .serializer import CategoriesSerializer, CostsSerializer
from .filters import IsOwnerFilterBackend
from apps.costs.models import Cost, CostCategory


class StandartCategoriesAPIView(ReadOnlyModelViewSet):
    """ Предоставляет список стандартных (общих) категорий  """
    queryset = CostCategory.objects.filter(is_custom=False)
    serializer_class = CategoriesSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = ('id', 'name')


class CustomCategoriesAPIViewSet(ModelViewSet):
    """ Предоставляет список категорий пользователя """
    queryset = CostCategory.objects.filter(is_custom=True)
    serializer_class = CategoriesSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (IsOwnerFilterBackend, DjangoFilterBackend)
    filterset_fields = ('id', 'name')

    def perform_create(self, serializer):
        # Устанавливаем текущего пользователя в поле "user" модели CostCategory
        serializer.save(user=self.request.user)


class CostsAPIViewSet(ModelViewSet):
    """ Предоставляет список затра пользователя с подробной информацией """
    queryset = Cost.objects.order_by('-date')
    serializer_class = CostsSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (IsOwnerFilterBackend, DjangoFilterBackend)
    filterset_fields = ('id', 'value', 'category__id', 'category__name', 'description')

    def perform_create(self, serializer):
        # Устанавливаем текущего пользователя в поле "user" модели Cost
        serializer.save(user=self.request.user)
