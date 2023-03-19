from django.contrib import admin
from .models import Reservation, Menu, Booking

# Register your models here.

admin.site.register(Reservation)
admin.site.register(Booking)
admin.site.register(Menu)
