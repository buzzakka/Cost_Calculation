from rest_framework import serializers
from costs.models import *


class StandartCategoriesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CostCategory
        fields = ['id', 'name']
