from rest_framework import generics
from costs.models import *
from .serializer import *


class StandartCategoriesAPIView(generics.ListAPIView):
    queryset = CostCategory.objects.filter(is_custom=False)
    serializer_class = StandartCategoriesSerializer
