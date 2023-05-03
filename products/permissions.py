from rest_framework import permissions
from .models import Product

class ProductSellerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_seller or request.user.is_superuser)