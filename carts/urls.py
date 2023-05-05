from django.urls import path
from . import views
from purchase_orders.views import PurchaseOrderDetalView


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
        PurchaseOrderDetalView.as_view(),
    ),
]
