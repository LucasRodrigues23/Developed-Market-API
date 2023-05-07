from rest_framework import serializers
from carts.models import CartListProducts
from .models import PurchaseOrders, OrderItems
from django.core.mail import send_mail
from django.conf import settings
from drf_spectacular.utils import (
    extend_schema_serializer,
    extend_schema_field,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes


class ProductCartSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    brand = serializers.CharField(allow_null=True)
    seller_id = serializers.UUIDField()


class ProductOrderListSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    brand = serializers.CharField(allow_null=True)
    seller_id = serializers.UUIDField()
    product_quantity = serializers.IntegerField()


class PurchaseOrdersListClientSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseOrders
        fields = [
            "id",
            "status",
            "price",
            "quantity_items",
            "user_id",
            "seller_id",
            "created_at",
            "updated_at",
            "products",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "price",
            "quantity_items",
            "products",
        ]

    @extend_schema_field(ProductOrderListSerializer)
    def get_products(self, validated_data):
        order_id = validated_data.id

        queryset_order_items = OrderItems.objects.filter(
            purchase_order=order_id
        ).select_related("product")

        list_order_items = [order_items for order_items in queryset_order_items]

        list_products = []
        for item in list_order_items:
            product_order = item.product.__dict__
            product_order["product_quantity"] = item.quantity
            list_products.append(product_order)

        list_products_serializer = ProductOrderListSerializer(
            data=list_products, many=True
        )
        list_products_serializer.is_valid(raise_exception=True)

        return list_products_serializer.data


@extend_schema_serializer(
    # exclude_fields=("sex",),
    examples=[
        OpenApiExample(
            "Exemplo Animal Serializer",
            summary="Criação de animais",
            description="Rota para criação de animais",
            value={
                "orders": [
                    {
                        "id": "f9cb24c1-0ef5-472e-adad-082b27248908",
                        "status": "Em Andamento",
                        "price": 1700.0,
                        "quantity_items": 2,
                        "client_id": "53823c8d-c5cc-4311-a4dc-0586e930ae5a",
                        "seller_id": "797c2e48-b070-42ca-ad95-c686b84a44c8",
                        "created_at": "2023-05-06T14:52:42.775926Z",
                        "updated_at": "2023-05-06T14:52:42.775948Z",
                        "products": [
                            {
                                "id": "57d1fe59-c647-483c-85c1-8d8162e6ddff",
                                "name": "Produto Ruim",
                                "description": "testestestestestes",
                                "price": "850.00",
                                "brand": "Marca Ruim",
                                "seller_id": "797c2e48-b070-42ca-ad95-c686b84a44c8",
                            }
                        ],
                    },
                    {
                        "id": "2fcf2d63-a33a-4b41-90fc-88e4906150e8",
                        "status": "Em Andamento",
                        "price": 198.0,
                        "quantity_items": 2,
                        "client_id": "53823c8d-c5cc-4311-a4dc-0586e930ae5a",
                        "seller_id": "50e4b827-bb03-416c-9b92-890273403d9a",
                        "created_at": "2023-05-06T14:52:43.731255Z",
                        "updated_at": "2023-05-06T14:52:43.731282Z",
                        "products": [
                            {
                                "id": "64f3f929-1416-4f06-ac24-259126d8e794",
                                "name": "Shorts Jeans",
                                "description": "Summer-essential cutoffs",
                                "price": "99.00",
                                "brand": "Denim",
                                "seller_id": "50e4b827-bb03-416c-9b92-890273403d9a",
                            }
                        ],
                    },
                ]
            },
            request_only=False,
            response_only=True,
        )
    ],
)
class PurchaseOrdersCreateSerializer(serializers.ModelSerializer):
    orders = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseOrders
        fields = ["id", "price", "quantity_items", "user_id", "seller_id", "orders"]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "price",
            "quantity_items",
            "orders",
        ]

    @extend_schema_field(PurchaseOrdersListClientSerializer)
    def get_orders(self, validated_data):
        list_orders = validated_data[0]
        list_cart_products = validated_data[1]

        orders = []
        for order in list_orders:
            list_product_order = [product for product in order.products.values()]

            list_product_order_serializer = ProductCartSerializer(
                data=list_product_order, many=True
            )
            list_product_order_serializer.is_valid(raise_exception=True)

            for product in list_product_order_serializer.data:
                for item in list_cart_products:
                    if str(product["id"]) == str(item.product.id):
                        product["quantity_product"] = item.quantity

            orders.append(
                {
                    "id": order.id,
                    "status": order.status,
                    "price": order.price,
                    "quantity_items": order.quantity_items,
                    "client_id": order.user.id,
                    "seller_id": order.seller.id,
                    "created_at": order.created_at,
                    "updated_at": order.updated_at,
                    "products": list_product_order_serializer.data,
                }
            )
        return orders

    def create(self, validated_data):
        cart_id = validated_data.pop("cart_id")

        cart_list = CartListProducts.objects.filter(cart_id=cart_id).select_related(
            "product"
        )

        if cart_list.count() == 0:
            raise serializers.ValidationError(
                {"message": "Sorry, your shopping cart is empty!"}
            )

        for item in cart_list:
            if item.product.is_available_for_sale is False:
                raise serializers.ValidationError(
                    {
                        "message": f"Sorry, the product {item.product.name} is not available!"
                    }
                )
            if item.quantity > item.product.quantity_stock:
                raise serializers.ValidationError(
                    {
                        "message": f"Sorry, the product {item.product.name} is not available!"
                    }
                )

        for item in cart_list:
            new_product_stock = item.product.quantity_stock - item.quantity
            item.product.quantity_stock = new_product_stock

            if new_product_stock == 0:
                item.product.is_available_for_sale = False
            item.product.save()

        seller_id_list = []
        for item in cart_list:
            if item.product.seller not in seller_id_list:
                seller_id_list.append(item.product.seller)

        order_list = []
        for seller in seller_id_list:
            validated_data["seller"] = seller
            price = 0
            quantity = 0
            for item in cart_list:
                if item.product.seller == seller:
                    price += item.quantity * item.product.price
                    quantity += item.quantity
            validated_data["quantity_items"] = quantity
            validated_data["price"] = price
            order = PurchaseOrders.objects.create(**validated_data)
            order_list.append(order)
            send_mail(
                subject=f"Pedido {order.id}",
                message=f"Pedido realizado com sucesso",
                from_email=settings.EMAIL_HOST,
                recipient_list=[order.user.email],
                fail_silently=False,
            )
        for item in cart_list:
            for order in order_list:
                if order.seller == item.product.seller:
                    OrderItems.objects.create(
                        quantity=item.quantity,
                        purchase_order=order,
                        product=item.product,
                    )

        cart_list.delete()
        return [order_list, cart_list]


class PurchaseOrdersUpdateSerializer(serializers.ModelSerializer):
    def update(self, instance: PurchaseOrders, validated_data: dict) -> PurchaseOrders:
        for key, value in validated_data.items():
            if key == "status":
                if instance.status == "Entregue":
                    raise serializers.ValidationError(
                        {"menssage": "the purchase order is already completed"}
                    )
                if instance.status == "Pedido Realizado" and value != "Entregue":
                    raise serializers.ValidationError(
                        {"menssage": "the purchase order is already acoomplished"}
                    )

                if instance.status == value:
                    raise serializers.ValidationError(
                        {"menssage": "the purchase order is already this status"}
                    )
                setattr(instance, key, value)

        instance.save()

        send_mail(
            subject=f"Pedido {instance.id}",
            message=f"O Status do seu pedido foi alterado para {instance.status}",
            from_email=settings.EMAIL_HOST,
            recipient_list=[instance.user.email],
            fail_silently=False,
        )

        return instance

    class Meta:
        model = PurchaseOrders
        fields = [
            "id",
            "status",
            "price",
            "quantity_items",
            "user_id",
            "seller_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "user_id",
            "seller_id",
            "price",
            "quantity_items",
            "products",
        ]
