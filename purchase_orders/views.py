from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import PurchaseOrders
from .serializer import PurchaseOrdersSerializer
""" from .permissions import IsOrderOwner """
from carts.models import Cart
from django.shortcuts import get_object_or_404


class PurchaseOrderDetalView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = PurchaseOrders
    serializer_class = PurchaseOrdersSerializer

    def perform_create(self, serializer):
        cart_exists = get_object_or_404(Cart, pk=self.kwargs.get("cart_id"))
        serializer.save(user=self.request.user, cart_id=self.kwargs.get("cart_id"))
        


""" class PurchaseOrderView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOrderOwner]

    def get_queryset(self):
        order_id = self.kwargs.get("order_id")
        order = get_object_or_404(PurchaseOrders, pk=order_id)
        return PurchaseOrders.objects.filter(order_id=order_id).select_related("product") """