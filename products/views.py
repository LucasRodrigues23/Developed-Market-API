from .models import Product
from users.models import User
from .serializers import ProductSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import ProductSellerPermission
from rest_framework.pagination import PageNumberPagination


class CustomPaginationProduct(PageNumberPagination):
    page_size = 10


class ProductView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [ProductSellerPermission]
    serializer_class = ProductSerializer
    pagination_class = CustomPaginationProduct

    def get_queryset(self):
        return Product.objects.all()

    def perform_create(self, serializer):
        return serializer.save(seller=self.request.user)
