from django.urls import path
from . import views


urlpatterns = [
    path(
        "orders/client/<uuid:user_id>/",
        views.PurchaseOrderListClientView.as_view(),
    ),
    path(
        "orders/seller/<uuid:user_id>/",
        views.PurchaseOrderListSellerView.as_view(),
    ),
    path(
        "orders/<uuid:pk>/seller/",
        views.PurchaseOrderDetailView.as_view(),
    ),
    path(
        "orders/sales-summary/seller/<uuid:pk>/",
        views.PurchaseOrderListGeneratePdfPdfView.as_view(),
    ),
]
