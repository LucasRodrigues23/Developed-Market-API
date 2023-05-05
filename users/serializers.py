from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from carts.models import Cart


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

    cpf = serializers.CharField(
        max_length=14,
        validators=[
            RegexValidator(
                regex=r"^\d{3}\.\d{3}\.\d{3}-\d{2}$",
                message="CPF inválido. Use o formato XXX.XXX.XXX-XX.",
                code="invalid_cpf",
            ),
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with that cpf already exists.",
            ),
        ],
    )

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        validators=[
            RegexValidator(
                regex=r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$",
                message="The password must  including at least one uppercase letter, one lowercase letter, one number, and one special character.",
                code="invalid_password",
            )
        ],
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
            "cpf",
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
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data: dict) -> User:
        is_superuser = validated_data.pop("is_superuser", None)

        if is_superuser:
            validated_data["is_seller"] = False
            validated_data["is_client"] = False
            new_superuser = User.objects.create_superuser(**validated_data)
            new_cart = Cart.objects.create(user=new_superuser)
            return new_superuser

        new_user = User.objects.create_user(**validated_data)
        new_cart = Cart.objects.create(user=new_user)
        return new_user

    def update(self, instance: User, validated_data: dict) -> User:
        ignore_keys = ["password", "username", "cpf", "is_superuser"]
        for key, value in validated_data.items():
            if not ignore_keys.__contains__(key):
                setattr(instance, key, value)

        if validated_data.get("password"):
            instance.set_password(validated_data["password"])

        instance.save()

        return instance


class CustomJWTSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["is_superuser"] = user.is_superuser
        token["is_seller"] = user.is_seller
        token["is_client"] = user.is_client

        return token
