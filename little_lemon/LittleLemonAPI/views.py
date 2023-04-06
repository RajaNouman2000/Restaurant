from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, throttle_classes, permission_classes
from rest_framework.views import APIView
from django.core.paginator import Paginator, EmptyPage

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from . throttles import TenCallsPerMinute

from rest_framework import status, generics
from rest_framework.permissions import (
    BasePermission, IsAuthenticated,    IsAdminUser,
    DjangoModelPermissionsOrAnonReadOnly, AllowAny)
from django.contrib.auth.models import User, Group

from . serializers import (
    MenuItemSerializer, GroupSerializer, UserSerializer,
    CartSerializer, OrderSerializer, OrderItemSerializer)
from . models import MenuItem, Cart, Order, OrderItem
from . permissions import IsNotManagerOrDelivery
# Create your views here.


class MenuItemsViews(generics.ListCreateAPIView):
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer

    ordering_fields = ['price', 'inventory']
    search_fields = ['title']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
            return [IsAdminUser()]
        return [AllowAny()]


class ManagerView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = GroupSerializer
    otherserializer_class = UserSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return self.serializer_class
        return self.otherserializer_class

    def get(self, request):
        group = Group.objects.get(name='Manager')
        users = group.user_set.all()
        user_list = [{'id': user.id, 'username': user.username}
                     for user in users]
        return Response({'users': user_list})

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create new user object
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name']
        )
        group = Group.objects.get(name='Manager')
        group.user_set.add(user)
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    ''' function to get admin Users
    def get(self, request):
        admin_users = User.objects.filter(is_staff=True)
        user_list = [{'id': user.id, 'username': user.username}
                     for user in admin_users]

        return Response({'admin_users': user_list})'''


class SingleManagerView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer

    def get(self, request, pk):
        group = Group.objects.get(name='Manager')
        user = group.user_set.filter(pk=pk).first()
        if user:
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        else:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)


class DeliveryCrewView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer

    def get(self, request):
        group = Group.objects.get(name='Delivery Crew')
        print(group)
        users = group.user_set.all()
        user_list = [{'id': user.id, 'username': user.username}
                     for user in users]
        print(user_list)
        return Response({'users': user_list})

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)

        # Create new user object
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name']
        )
        group = Group.objects.get(name='Delivery Crew')
        group.user_set.add(user)
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SingleDeliveryCrewView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer

    def get(self, request, pk):
        group = Group.objects.get(name='Delivery Crew')
        user = group.user_set.filter(pk=pk).first()
        print(group.user_set.filter(pk=pk))

        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serialized_user = self.serializer_class(user).data
        return Response(serialized_user)


class CartView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)

    def perform_create(self, serializer):
        menuitem = self.request.data.get('menuitem')
        quantity = self.request.data.get('quantity')
        unit_price = MenuItem.objects.get(pk=menuitem).price
        quantity = int(quantity)
        price = quantity * unit_price
        serializer.save(user=self.request.user, price=price)

    def delete(self, request):
        user = self.request.user
        Cart.objects.filter(user=user).delete()
        return Response(status=204)


class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = OrderItem.objects.all()
