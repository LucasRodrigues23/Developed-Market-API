from rest_framework import serializers
from .models import CarListProducts


class CartListProductsSerializer(serializers.ModelSerializer):

    class Meta:

        model = CarListProducts
        fields = ["id", "quantity", "cart_id", "product_id"]
        read_only_fields = ["id"]

        def create(self, validated_data: dict) -> CartListProducts:
            return CarListProducts.objects.create(**validated_data)