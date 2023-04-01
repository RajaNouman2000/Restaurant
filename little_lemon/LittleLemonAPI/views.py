from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view, throttle_classes, permission_classes
from rest_framework.views import APIView
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from . throttles import TenCallsPerMinute


from . serializers import MenuItemSerializer
from . models import MenuItem


# Create your views here.





class MenuItemsViews(generics.ListCreateAPIView):
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'inventory']
    search_fields = ['title']


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


