from rest_framework import serializers
from .models import Product, CategoryOptions


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(choices=CategoryOptions.choices)

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
        read_only_fields = [
            "id",
            "is_available_for_sale",
            "created_at",
            "updated_at",
            "seller_id",
        ]
    def validate_category(self, value):
        choices = dict(self.CategoryOptions.choices)
        if value not in choices:
            raise serializers.ValidationError(
                f"The available categories are: {', '.join(choices.values())}"
            )
        return value
        

    def create(self, validated_data):
        if validated_data["quantity_stock"] > 0:
            validated_data["is_available_for_sale"] = True

        return Product.objects.create(**validated_data)

    def update(self, instance: Product, validated_data: dict) -> Product:
        for key, value in validated_data.items():
            if key == "quantity_stock":
                setattr(instance, key, value)
        instance.save()
        return instance
