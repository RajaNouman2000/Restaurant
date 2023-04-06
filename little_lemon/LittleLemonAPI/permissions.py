
from rest_framework.permissions import BasePermission


class IsNotManagerOrDelivery(BasePermission):
    def has_permission(self, request, view):
        return not (request.user.groups.filter(name='Manager').exists() or request.user.groups.filter(name='Delivery Crew').exists())
