from django.shortcuts import render
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


def index(request):
    return render(request, 'index.html')


def display_menu_item(request, pk):
    if pk:
        menu_item = Menu.objects.get(pk=pk)
    else:
        menu_item = ''
    return render(request, "menu_item.html", {"menu_item": menu_item})
