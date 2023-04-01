from django.contrib import admin
from .models import Category, MenuItem, OrderItem, Cart, Order

# Register your models here.

admin.site.register(MenuItem)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
