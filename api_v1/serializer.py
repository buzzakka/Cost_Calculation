from rest_framework import serializers
from costs.models import *


class CategoriesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CostCategory
        fields = ['id', 'name']
