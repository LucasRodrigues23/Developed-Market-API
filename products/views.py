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
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPaginationProduct

    def get_queryset(self):
        route_parameter_id = self.request.query_params.get("id")
        route_parameter_name = self.request.query_params.get("name")
        route_parameter_category = self.request.query_params.get("category")

        if route_parameter_id:
            queryset = Product.objects.filter(id__iexact=route_parameter_id)
            return queryset
        
        if route_parameter_name:
            queryset = Product.objects.filter(name__icontains=route_parameter_name)
            return queryset
        
        if route_parameter_category:
            queryset = Product.objects.filter(category__iexact=route_parameter_category)
            return queryset
        
        return super().get_queryset()
    

    def perform_create(self, serializer):
        return serializer.save(seller=self.request.user)
