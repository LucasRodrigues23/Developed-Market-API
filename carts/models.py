from django.db import models
import uuid


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="cart"
    )

    products = models.ManyToManyField(
        "products.Product", through="CartListProducts", related_name="carts"
    )


class CartListProducts(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    quantity = models.IntegerField()

    cart = models.ForeignKey(
        "carts.Cart",
        on_delete=models.CASCADE,
        related_name="cart_list"
    )

    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="cart_list"
    )
