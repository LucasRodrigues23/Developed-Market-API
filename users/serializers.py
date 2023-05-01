from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with that username already exists.",
            )
        ],
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User

        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "password",
            "email",
            "bio",
            "birthdate",
            "is_superuser",
            "is_seller",
            "is_client",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            # "is_superuser",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data: dict) -> User:
        is_superuser = validated_data.pop("is_superuser", None)

        if is_superuser:
            return User.objects.create_superuser(**validated_data)

        if validated_data["is_client"] is True:
            return User.objects.create_user(**validated_data)

        return User.objects.create_user(**validated_data)
