from django.urls import path
from .views import about, menu_by_id

urlpatterns = [
    path('', about, name='about'),
    path('menucard/', menu_by_id, name='menu'),

]
