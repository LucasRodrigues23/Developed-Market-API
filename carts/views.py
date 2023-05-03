from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import CartListProducts
from .serializers import CartListProductsSerializer


class CartListProductsView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = CartListProducts.objects.all()
    serializer_class = CartListProductsSerializer

    def perform_create(self, serializer):
        return serializer.save(
            cart_id=self.kwargs.get("cart_id"),
            product_id=self.request.data["product_id"],
        )
