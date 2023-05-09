from rest_framework import permissions
from users.models import User
from rest_framework.views import View
from .models import PurchaseOrders


class IsOrdersOwner(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        user_id = request.path.split("/")[4]
        return request.user.is_authenticated and (str(user_id) == str(request.user.id))


class IsOrderProductOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: PurchaseOrders) -> bool:
        return (
            request.user.is_authenticated
            and obj.seller_id == request.user.id
            or request.user.is_superuser
        )


class IsSalesSummaryOwner(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        user_id = request.path.split("/")[5]

        return (
            request.user.is_authenticated
            and request.user.is_seller == True
            and (str(user_id) == str(request.user.id))
        )
