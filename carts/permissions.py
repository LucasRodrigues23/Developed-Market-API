from rest_framework import permissions
from .models import Cart
from rest_framework.views import View


class IsCartOwner(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.user.is_superuser:
            return True
        cart_id = request.path.split("/")[3]
        cart_owner = Cart.objects.filter(pk=cart_id, user_id=request.user.id).exists()
        return cart_owner


class IsCartListOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj) -> bool:
        return (
            request.user.is_authenticated
            and obj.user_id == request.user.id
            or request.user.is_superuser
        )
