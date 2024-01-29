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

    def create(self, request, *args, **kwargs):
        response = super(CustomCategoriesAPIViewSet, self).create(request, *args, **kwargs)
        response.data['user'] = self.request.user
        return Response(response)


class CostsAPIViewSet(ModelViewSet):
    """
        Предоставляет список затра пользователя с подробной информацией
    """
    queryset = Cost.objects.order_by('-date')
    serializer_class = CostsSerializer
    filter_backends = (IsOwnerFilterBackend, DjangoFilterBackend)
    filterset_fields = ('id', 'value', 'category', 'description')
