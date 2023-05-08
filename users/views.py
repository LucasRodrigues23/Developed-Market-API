from .models import User
from .serializers import UserSerializer, CustomJWTSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsAccountOwner
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Users", "Autenticação", "Products", "Carts", "Orders"])
@extend_schema(
    tags=["Users"],
)
class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@extend_schema(
    tags=["Users"],
)
@extend_schema(
    description="testando a descrição por rota GET",
    methods=["GET"],
)
@extend_schema(
    description="testando a descrição por rota PATCH",
    methods=["PATCH"],
)
@extend_schema(
    description="testando a descrição por rota PUT",
    methods=["PUT"],
)
class UserDetailView(RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
    queryset = User.objects.all()
    serializer_class = UserSerializer


@extend_schema(
    tags=["Autenticação"],
)
class LoginJWTView(TokenObtainPairView):
    serializer_class = CustomJWTSerializer


@extend_schema(tags=["Autenticação"])
class MyTokenRefreshView(TokenRefreshView):
    pass
