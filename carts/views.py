from rest_framework.generics import CreateAPIView
from .models import CartListProducts
from .serializers import CartListProductsSerializer
from .permissions import IsCartOwner


class CartListProductsView(CreateAPIView):
    permission_classes = [IsCartOwner]
    queryset = CartListProducts.objects.all()
    serializer_class = CartListProductsSerializer

    def perform_create(self, serializer):
        return serializer.save(
            cart_id=self.kwargs.get("cart_id"),
            product_id=self.request.data["product_id"],
        )
