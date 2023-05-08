from django.urls import path
from . import views
from purchase_orders.views import PurchaseOrderCreateView


urlpatterns = [
    path(
        "carts/<uuid:cart_id>/products/",
        views.CartListProductsView.as_view(),
    ),
    path(
        "carts/<uuid:cart_id>/",
        views.CartRetrieve.as_view(),
    ),
    path(
        "carts/<uuid:cart_id>/orders/",
        PurchaseOrderCreateView.as_view(),
    ),
    path(
        "carts/<uuid:pk>/product/<uuid:product_id>/",
        views.RemoveProduct.as_view(),
    ),
]
