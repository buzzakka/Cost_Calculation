from rest_framework import serializers
from apps.costs.models import Cost, CostCategory

class CategoriesSerializer(serializers.ModelSerializer):
    """ Сериализатор для категорий трат """
    class Meta:
        model = CostCategory
        fields = ('id', 'name')


class CostsSerializer(serializers.ModelSerializer):
    """ Сериализатор для затрат пользователя """
    # category = CategoriesSerializer(read_only=True)

    class Meta:
        model = Cost
        fields = ('id', 'value', 'category', 'date', 'description')
