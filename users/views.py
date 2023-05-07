from .models import User
from .serializers import UserSerializer, CustomJWTSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsAccountOwner
from drf_spectacular.utils import extend_schema


class UserCreateView(CreateAPIView):
    permission_classes = []

    queryset = User.objects.all()
    serializer_class = UserSerializer


@extend_schema(description="testando a descrição por rota GET", methods=["GET"])
@extend_schema(description="testando a descrição por rota PATCH", methods=["PATCH"])
@extend_schema(description="testando a descrição por rota PUT", methods=["PUT"])
class UserDetailView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAccountOwner]


class LoginJWTView(TokenObtainPairView):
    serializer_class = CustomJWTSerializer
