from .models import User
from .serializers import UserSerializer, CustomJWTSerializer
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated


class UserCreateView(CreateAPIView):
    permission_classes = []

    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginJWTView(TokenObtainPairView):
    serializer_class = CustomJWTSerializer
