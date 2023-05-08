from .models import Address
from .serializers import AddressSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Users"],
)
class AddressCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
