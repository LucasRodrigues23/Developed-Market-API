from rest_framework import permissions
from users.models import User
from rest_framework.views import View


class IsOrdersOwner(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        if request.user.is_superuser:
            return True
        user_id = request.path.split("/")[4]
        return str(user_id) == str(request.user.id)


class IsProductOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        print(request.user)
        return (
            request.user.is_authenticated
            and request.user.is_seller
            or request.user.is_superuser
        )
