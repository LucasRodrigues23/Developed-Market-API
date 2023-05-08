from rest_framework import permissions
from users.models import User
from .models import Address


class IsAddressCreatePermissionr(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        user_id = request.path.split("/")[4]
        user_owner = User.objects.filter(pk=user_id).exists()
        return (
            request.user.is_authenticated
            and user_owner
            and (str(user_id) == str(request.user.id))
        )


class IsAddressOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Address) -> bool:
        return (
            request.user.is_authenticated
            and obj.user_id == request.user.id
            or request.user.is_superuser
        )
