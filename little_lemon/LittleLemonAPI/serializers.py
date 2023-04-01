from rest_framework import serializers
from decimal import Decimal
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User
import bleach

from .models import MenuItem
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']


class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    # category = CategorySerializer(many=True)
    def validate_title(self, value):
        return bleach.clean(value)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'stock',
                  'price_after_tax', 'category']
        extra_kwargs = {
            'price': {'min_value': 2},
            # 'inventory': {'min_value': 0},
            'stock': {'source': 'inventory', 'min_value': 0}
        }

        depth = 1

    def calculate_tax(self, product: MenuItem):
        return product.price * Decimal(1.1)
