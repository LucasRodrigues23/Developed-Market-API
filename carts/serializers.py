from rest_framework import serializers
from .models import CartListProducts, Cart
from products.models import Product


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


class CartRetrieveSerializer(serializers.ModelSerializer):
    total_product = serializers.SerializerMethodField()
    product = ProductCartListSerializer()

    class Meta:
        model = CartListProducts
        fields = ["quantity", "total_product", "product"]
        read_only_fields = ["id"]
        depth = 1

    def get_total_product(self, validated_data):
        return validated_data.quantity * validated_data.product.price
