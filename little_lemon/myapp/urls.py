from django.urls import path
from . import views

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items', views.MenuItemsViews.as_view()),
    # path('menu-items', views.menu_item),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('book/', views.booking, name='booking'),
    path('menu/', views.menu, name='menu'),
    path('menu_item/<int:pk>/', views.display_menu_item, name="menu_item"),
    path('api-token-auth', obtain_auth_token),
    path('secret', views.secret),
    path('throttle-check', views.throttle_check),
    path('throttle-check-user', views.throttle_check_user)
]
