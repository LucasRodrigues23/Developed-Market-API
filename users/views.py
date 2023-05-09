from .models import User
from .serializers import UserSerializer, CustomJWTSerializer
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
    ListAPIView,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsAccountOwner
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


@extend_schema(
    tags=["Users"],
    description="""Cria um usuário, podendo ser admin, 
     seller ou client.""",
)
class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@extend_schema(
    tags=["Users"],
)
@extend_schema(
    description="""Listar informações do usuário, a partir do id
    informado no parâmetro da rota. O usuário logado precisa ser 
    admin ou dono das informações.""",
    methods=["GET"],
)
@extend_schema(
    description="""Atualizar as informações do usuário, a partir do id
    informado no parâmetro da rota. O usuário logado precisa ser 
    admin ou dono das informações.""",
    methods=["PATCH"],
)
@extend_schema(
    methods=["PUT"],
    exclude=True,
)
class UserDetailView(RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
    queryset = User.objects.all()
    serializer_class = UserSerializer


@extend_schema(
    tags=["Autenticação"],
    description="""Utiliza das credencias do usuário (username e password),
    para realizar autenticação e retorna dois tokens, um de acesso e outro de 
    atualização.""",
)
class LoginJWTView(TokenObtainPairView):
    serializer_class = CustomJWTSerializer


@extend_schema(
    tags=["Autenticação"],
    description="""Utiliza do token de atualização, para gerar um novo token 
    de acesso.""",
)
class MyTokenRefreshView(TokenRefreshView):
    pass


class CustomPaginationUserProfile(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(data[0])


@extend_schema(
    tags=["Users"],
    description="""Listar informações do usuário logado.""",
)
class UserProfileView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    pagination_class = CustomPaginationUserProfile

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.id)
