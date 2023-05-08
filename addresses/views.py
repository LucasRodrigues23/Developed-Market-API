from .models import Address
from .serializers import AddressSerializer
from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAddressCreatePermissionr


@extend_schema(
    tags=["Users"],
)
class AddressCreateView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAddressCreatePermissionr]

    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.kwargs.get("user_id"))
