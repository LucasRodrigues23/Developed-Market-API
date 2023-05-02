from rest_framework.views import APIView, status, Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView


class ProductView(ListCreateAPIView, PageNumberPagination):
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductSerializer
    page_size = 2

    def get_queryset(self):
        return Product.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()
    
    