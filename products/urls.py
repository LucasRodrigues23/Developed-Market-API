from django.urls import path
from . import views
from products.views import ProductView
from products import views as product_views

urlpatterns = [
    path("products/", views.ProductView.as_view()),
    path("products/<uuid:pk>/", product_views.StockProductUpdateView.as_view()),
]
