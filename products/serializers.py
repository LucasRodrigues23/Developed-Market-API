from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    is_available_for_sale = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "quantity_stock",
            "is_available_for_sale",
            "brand",
            "category",
            "seller_id",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "seller_id"]

    def get_is_available_for_sale(self, validated_data):
        if validated_data.quantity_stock > 0:
            return True
        else:
            return False

    def create(self, validated_data):
        return Product.objects.create(**validated_data)
