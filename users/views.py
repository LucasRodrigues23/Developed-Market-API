from django.shortcuts import render
from .models import User
from .serializers import UserSerializer
from rest_framework.generics import CreateAPIView


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
