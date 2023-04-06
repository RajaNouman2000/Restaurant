from rest_framework import serializers
from decimal import Decimal
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User, Group
import bleach

from .models import (
    MenuItem, Cart, Category, Order, OrderItem
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']


class MenuItemSerializer(serializers.ModelSerializer):
    price_after_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    # category = CategorySerializer(many=True)
    def validate_title(self, value):
        return bleach.clean(value)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured',
                  'price_after_tax', 'category']
        extra_kwargs = {
            'price': {'min_value': 2},
            # 'inventory': {'min_value': 0},
            'stock': {'source': 'inventory', 'min_value': 0}
        }

        depth = 1

    def calculate_tax(self, product: MenuItem):
        return product.price * Decimal(1.1)


class CartSerializer(serializers.ModelSerializer):
    unit_price = serializers.DecimalField(
        max_digits=6, decimal_places=2, source='menuitem.price', read_only=True)
    name = serializers.CharField(source='menuitem.title', read_only=True)

    class Meta:
        model = Cart
        fields = ['user_id', 'menuitem', 'name',
                  'quantity', 'unit_price', 'price']
        extra_kwargs = {
            'price': {'read_only': True}
        }


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    group = {'Manager': 'Manager',
             'Delivery Crew': 'Delivery Crew'}

    class Meta:
        model = User
        fields = ['username', 'first_name',
                  'last_name', 'email', 'password']
