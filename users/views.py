from .models import User
from .serializers import UserSerializer, CustomJWTSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAccountOwner


class UserCreateView(CreateAPIView):
    permission_classes = []

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAccountOwner]


class LoginJWTView(TokenObtainPairView):
    serializer_class = CustomJWTSerializer
