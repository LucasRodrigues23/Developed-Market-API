from rest_framework.views import APIView, status, Response
from .models import Product
from users.models import User
from .serializers import ProductSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ProductView(ListCreateAPIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductSerializer
    page_size = 2
    
    def get_queryset(self):
        return Product.objects.all()
    
    def perform_create(self, serializer):
        return serializer.save(seller=self.request.user)
    
    