from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view, throttle_classes, permission_classes
from rest_framework.views import APIView
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from . throttles import TenCallsPerMinute

from . models import Menu
from . serializers import MenuItemSerializer
from . models import MenuItem

# Create your views here.

""""
@api_view(['GET', 'POST'])
def menu_item(request):
    if (request.method == 'GET'):
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        # print(category_name)
        to_price = request.query_params.get('price')
        # print(to_price)
        search = request.query_params.get('search')
        # print(search)
        ordering = request.query_params.get('ordering')
        # print(search)

        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)
        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price=to_price)
        if search:
            items = items.filter(title__startswith=search)
        if ordering:
            ordering_fields = ordering.split(',')
            items = items.order_by(*ordering_fields)

        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []

        serialized_item = MenuItemSerializer(items, many=True)
        return Response(serialized_item.data)

    elif (request.method == 'POST'):
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.validated_data, status.HTTP_201_CREATED)
"""


@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message": "Some secret message"})


@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.group.filter(name='Manager').exist():
        return Response({"message": "Only Manager Should See this"})
    else:
        return Response({"message": "You are not authorized"})


@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message": "Successful"})


@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def throttle_check_user(request):
    return Response({"message": "Successful!!!"})


class MenuItemsViews(generics.ListCreateAPIView):
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'inventory']
    search_fields = ['title']


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


def home(request):
    return render(request, 'home.html')


def booking(request):
    return render(request, 'book.html')


def about(request):
    return render(request, 'about.html')


def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', main_data)


class Menu(APIView):
    def get(self, request):
        menu_name = request.GET.get('name')
        return Response({"message": "list of the menu"+menu_name}, status.HTTP_200_OK)

    def post(self, request):

        return Response({"message": "list of the menu"}, status.HTTP_200_OK)


def display_menu_item(request, pk):
    if pk:
        menu_item = Menu.objects.get(pk=pk)
    else:
        menu_item = ''
    return render(request, "menu_item.html", {"menu_item": menu_item})
