from rest_framework import serializers
from .models import CartListProducts, Cart
from products.models import Product
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema_serializer,
    extend_schema_field,
    OpenApiExample,
)


class CartListProductsSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField(format="hex_verbose")

    class Meta:
        model = CartListProducts
        fields = ["id", "quantity", "cart_id", "product_id"]
        read_only_fields = ["id"]

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError({"message": "product not found!"})
        return value

    def create(self, validated_data: dict) -> CartListProducts:
        if not Cart.objects.filter(pk=validated_data["cart_id"]).exists():
            raise serializers.ValidationError({"message": "cart not found!"})
        find_cart = CartListProducts.objects.filter(
            cart_id=validated_data["cart_id"], product_id=validated_data["product_id"]
        ).first()
        if find_cart:
            new_quantity = find_cart.quantity + validated_data["quantity"]
            find_cart.quantity = new_quantity
            find_cart.save()
            return find_cart
        else:
            return CartListProducts.objects.create(**validated_data)


class ProductCartListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "brand",
            "category",
            "seller_id",
        ]


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Example list cart",
            summary="List Cart",
            value={
                "id": "fbf8e423-e82a-4f44-a82d-493873ce6a63",
                "total_value_cart": 159.9,
                "cart_list": [
                    {
                        "quantity": 2,
                        "total_product": 24.36,
                        "product": {
                            "id": "b7f3f2ec-0c9b-4200-b650-6c02775845db",
                            "name": "teste2",
                            "description": "testestestestestes",
                            "price": "12.18",
                            "brand": "teste",
                            "category": "Others",
                            "seller_id": "513a656c-9f96-4847-9cb1-5aa3ff534996",
                        },
                    },
                    {
                        "quantity": 3,
                        "total_product": 135.54,
                        "product": {
                            "id": "a359a2dd-2c80-44a8-9921-1361032d794d",
                            "name": "teste3",
                            "description": "testestestestestes",
                            "price": "45.18",
                            "brand": "teste",
                            "category": "Others",
                            "seller_id": "513a656c-9f96-4847-9cb1-5aa3ff534996",
                        },
                    },
                ],
            },
            request_only=False,
            response_only=True,
        )
    ],
)
class CartRetrieveSerializer(serializers.ModelSerializer):
    total_product = serializers.SerializerMethodField()
    product = ProductCartListSerializer()

    class Meta:
        model = CartListProducts
        fields = ["quantity", "total_product", "product"]
        read_only_fields = ["id"]
        depth = 1

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_total_product(self, validated_data):
        return validated_data.quantity * validated_data.product.price
