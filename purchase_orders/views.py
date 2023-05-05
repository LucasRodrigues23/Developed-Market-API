from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import PurchaseOrders
from .serializer import (
    PurchaseOrdersCreateSerializer,
    PurchaseOrdersListClientSerializer,
)
from carts.models import Cart
from users.models import User
from django.shortcuts import get_object_or_404
from carts.permissions import IsCartOwner


class PurchaseOrderCreateView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCartOwner]
    queryset = PurchaseOrders
    serializer_class = PurchaseOrdersCreateSerializer

    def perform_create(self, serializer):
        cart_exists = get_object_or_404(Cart, pk=self.kwargs.get("cart_id"))
        serializer.save(user=self.request.user, cart_id=self.kwargs.get("cart_id"))


class PurchaseOrderListClientView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = PurchaseOrdersListClientSerializer
    # permission_classes = [IsOrderOwner]

    def get_queryset(self):
        client_id = self.kwargs.get("client_id")
        order = get_object_or_404(User, pk=client_id)
        return PurchaseOrders.objects.filter(user_id=client_id).order_by("updated_at")
