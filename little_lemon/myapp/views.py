from django.shortcuts import render
from .models import Menu
# Create your views here.


def about(request):
    return render(request, 'about.html')


def menu_by_id(request):
    new_menu = Menu.objects.all()
    new_menu_dict = {"menu": new_menu}
    return render(request, "menu_card.html", new_menu_dict)
