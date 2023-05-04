from django.db import models
import uuid


class StatusChoices(models.TextChoices):
    DEFAULT = "Em Andamento"
    ACOOMPLISHED = "Pedido Realizado"
    DELIVERED = "Entregue"


class PurchaseOrders(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    status = models.CharField(
        max_length=50, choices=StatusChoices.choices, default=StatusChoices.DEFAULT
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_items = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="purchase_orders_client",
    )
    seller = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="purchase_orders_seller",
    )
    products = models.ManyToManyField(
        "products.Product",
        related_name="purchase_orders"
    )
