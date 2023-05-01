from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views
from addresses.views import AddressCreateView

urlpatterns = [
    path("users/", views.UserCreateView.as_view()),
    path("users/address/", AddressCreateView.as_view()),
    path("login/", views.LoginJWTView.as_view()),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view()),
]
