from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views
from addresses.views import AddressCreateView

urlpatterns = [
    path("users/", views.UserCreateView.as_view()),
    path("users/<uuid:pk>/", views.UserDetailView.as_view()),
    path("users/address/", AddressCreateView.as_view()),
    path("login/", views.LoginJWTView.as_view()),
    path("token/refresh/", views.MyTokenRefreshView.as_view()),
]
