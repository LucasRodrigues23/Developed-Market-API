from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import PurchaseOrders
from .serializer import (
    PurchaseOrdersCreateSerializer,
    PurchaseOrdersListClientSerializer,
    PurchaseOrdersUpdateSerializer,
)
from carts.models import Cart
from users.models import User
from django.shortcuts import get_object_or_404
from carts.permissions import IsCartOwner
from .permissions import IsOrdersOwner, IsOrderProductOwner


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
    permission_classes = [IsOrdersOwner]
    serializer_class = PurchaseOrdersListClientSerializer

    def get_queryset(self):
        client_id = self.kwargs.get("user_id")
        order = get_object_or_404(User, pk=client_id)
        if self.request.path.__contains__("seller"):
            return PurchaseOrders.objects.filter(seller_id=client_id).order_by(
                "updated_at"
            )
        return PurchaseOrders.objects.filter(user_id=client_id).order_by("updated_at")


class PurchaseOrderDetailView(RetrieveUpdateAPIView):
    permission_classes = [IsOrderProductOwner]
    queryset = PurchaseOrders.objects.all()
    serializer_class = PurchaseOrdersUpdateSerializer
