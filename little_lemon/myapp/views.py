from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .models import Menu
# Create your views here.


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
