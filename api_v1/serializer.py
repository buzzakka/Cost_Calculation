from rest_framework import serializers
from costs.models import *


class CategoriesSerializer(serializers.HyperlinkedModelSerializer):
    """
        Сериализатор для категорий трат
    """
    class Meta:
        model = CostCategory
        fields = ('id', 'name')


class CostsSerializer(serializers.HyperlinkedModelSerializer):
    """
        Сериализатор для затрат пользователя
    """
    category = CategoriesSerializer(read_only=True)

    class Meta:
        model = Cost
        fields = ('id', 'value', 'category', 'date', 'description')
