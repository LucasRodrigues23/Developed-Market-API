from django.shortcuts import render
from .models import User
from .serializers import UserSerializer, CustomJWTSerializer
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginJWTView(TokenObtainPairView):
    serializer_class = CustomJWTSerializer
