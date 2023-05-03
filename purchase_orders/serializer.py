from rest_framework import serializers

from .models import CartListProducts


class CartListProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartListProducts
        fields = ["id", "status", "quantity", "user", "product"]

    def create(self, validated_data):
        return CartListProductsSerializer.objects.create(**validated_data)
