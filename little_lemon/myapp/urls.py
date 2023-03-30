from django.urls import path
from . import views

urlpatterns = [
    path('menu-items', views.MenuItemsViews.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('book/', views.booking, name='booking'),
    path('menu/', views.menu, name='menu'),
    path('menu_item/<int:pk>/', views.display_menu_item, name="menu_item"),
]
