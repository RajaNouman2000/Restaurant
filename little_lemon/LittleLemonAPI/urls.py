from django.urls import path
from . import views

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items', views.MenuItemsViews.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),

    path('api-token-auth', obtain_auth_token),

]
