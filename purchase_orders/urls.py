from django.urls import path
from . import views


urlpatterns = [
    path(
        "orders/client/<uuid:client_id>/",
        views.PurchaseOrderListClientView.as_view(),
    ),
    # path(
    #     "carts/<uuid:cart_id>/",
    #     views.CartRetrieve.as_view(),
    # ),
    # path(
    #     "carts/<uuid:cart_id>/orders/",
    #     PurchaseOrderDetalView.as_view(),
    # ),
]
