from django.urls import path
from . import views
from addresses.views import AddressCreateView, AddressUpdateView

urlpatterns = [
    path("users/", views.UserCreateView.as_view()),
    path("users/<uuid:pk>/", views.UserDetailView.as_view()),
    path("users/<uuid:user_id>/address/", AddressCreateView.as_view()),
    path("users/address/<uuid:pk>/", AddressUpdateView.as_view()),
    path("users/profile/", views.UserProfileView.as_view()),
    path("login/", views.LoginJWTView.as_view()),
    path("token/refresh/", views.MyTokenRefreshView.as_view()),
]
