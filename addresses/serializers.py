from rest_framework import serializers
from .models import Address
from django.core.validators import RegexValidator


class AddressSerializer(serializers.ModelSerializer):
    cep = serializers.CharField(
        max_length=9,
        validators=[
            RegexValidator(
                regex=r"^\d{5}-\d{3}$",
                message="CEP inválido. Use o formato XXXXX-XXX.",
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
        return Address.objects.create_user(**validated_data)
