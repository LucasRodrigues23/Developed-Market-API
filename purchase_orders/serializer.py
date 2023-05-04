from rest_framework import serializers
from carts.models import CartListProducts

from .models import PurchaseOrders


class PurchaseOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrders
        fields = ["id","price", "quantity_items","user_id", "seller_id"]
        read_only_fields = ["id", "created_at", "updated_at", "price", "quantity_items"]

    def create(self, validated_data):
        cart_id = validated_data.pop("cart_id")
        
        cart_list =  CartListProducts.objects.filter(cart_id=cart_id).select_related("product")
        if cart_list.count() == 0:
            raise serializers.ValidationError({"message":"Sorry, your shopping cart is empty!"})
        seller_id_list = []
        for item in cart_list:
            if not item.product.seller in seller_id_list:
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
        for item in cart_list:
            for order in order_list:
                if order.seller == item.product.seller:
                    order.products.add(item.product)

        for item in cart_list:
            item.delete()
        return order_list[0]


