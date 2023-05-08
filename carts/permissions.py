from rest_framework import permissions
from .models import Cart


class IsCartOwner(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.user.is_superuser:
            return True
        cart_id = request.path.split("/")[3]
        cart_owner = Cart.objects.filter(pk=cart_id, user_id=request.user.id).exists()
        return cart_owner
