from rest_framework import serializers
from .models import Address
from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator


class AddressSerializer(serializers.ModelSerializer):
    cep = serializers.CharField(
        max_length=9,
        validators=[
            RegexValidator(
                regex=r"^\d{5}-\d{3}$",
                message="Invalid ZIP code format. Use the format XXXXX-XXX.",
                code="invalid_cep",
            )
        ],
    )

    class Meta:
        model = Address

        fields = [
            "id",
            "country",
            "state",
            "city",
            "district",
            "street",
            "number",
            "cep",
            "complement",
            "updated_at",
            "user_id",
        ]
        read_only_fields = [
            "id",
            "user_id",
            "updated_at",
        ]

    def create(self, validated_data: dict) -> Address:
        user_id = validated_data.get("user_id")
        if Address.objects.filter(user_id=user_id).exists():
            raise serializers.ValidationError(
                {"message": "User already has a registered address."}
            )
        return Address.objects.create(**validated_data)
