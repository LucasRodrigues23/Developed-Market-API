from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from .models import CartListProducts, Cart
from .serializers import CartListProductsSerializer, CartRetrieveSerializer
from .permissions import IsCartOwner
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from products.models import Product


class CustomPaginationCartRetrieve(PageNumberPagination):
    def get_paginated_response(self, data):
        cart_id = self.request.path.split("/")[3]
        total_value_cart = 0
        for product in data:
            total_value_cart += product["total_product"]
        return Response(
            {"id": cart_id, "total_value_cart": total_value_cart, "cart_list": data}
        )


@extend_schema(
    tags=["Carts"],
)
class CartListProductsView(CreateAPIView):
    permission_classes = [IsCartOwner]
    queryset = CartListProducts.objects.all()
    serializer_class = CartListProductsSerializer

    def perform_create(self, serializer):
        return serializer.save(
            cart_id=self.kwargs.get("cart_id"),
            product_id=self.request.data["product_id"],
        )


@extend_schema(
    tags=["Carts"],
)
class CartRetrieve(ListAPIView):
    permission_classes = [IsCartOwner]
    serializer_class = CartRetrieveSerializer
    pagination_class = CustomPaginationCartRetrieve

    def get_queryset(self):
        cart_id = self.kwargs.get("cart_id")
        cart = get_object_or_404(Cart, pk=cart_id)
        return CartListProducts.objects.filter(cart_id=cart_id).select_related(
            "product"
        )


@extend_schema(
    tags=["Carts"],
)
class RemoveProduct(DestroyAPIView):
    permission_classes = [IsCartOwner]
    queryset = Cart.objects.all()
    serializer_class = CartRetrieveSerializer

    def perform_destroy(self, instance):
        product_id = self.kwargs["product_id"]
        cart_id = self.kwargs["pk"]
        product = get_object_or_404(Product, id=product_id)
        cart_product = CartListProducts.objects.filter(
            product_id=product_id, cart_id=cart_id
        )

        cart_product.delete()
