from django.db import models
import uuid


class StatusChoices(models.TextChoices):
    DEFAUL = "Em Andamento"
    ACOOMPLISHED = "Pedido Realizado"
    DELIVERED = "Entregue"


class PurchaseOrders(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    status = models.ChoiceFiled(choices=StatusChoices, default=StatusChoices.DEFAULT)
    quantity = models.IntegerField()
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="purchase_orders",
    )

    products = models.ForeignKey(
        "products.Product",
        related_name="purchase_orders",
    )
