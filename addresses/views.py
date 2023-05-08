from .models import Address
from .serializers import AddressSerializer
from rest_framework.generics import CreateAPIView, UpdateAPIView
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAddressCreatePermissionr, IsAddressOwner


@extend_schema(
    tags=["Address"],
)
class AddressCreateView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAddressCreatePermissionr]

    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.kwargs.get("user_id"))


@extend_schema(
    tags=["Address"],
)
class AddressUpdateView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAddressOwner]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
