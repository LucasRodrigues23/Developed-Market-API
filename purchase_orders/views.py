from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
    RetrieveAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import PurchaseOrders
from .serializer import (
    PurchaseOrdersCreateSerializer,
    PurchaseOrdersListClientSerializer,
    PurchaseOrdersUpdateSerializer,
)
from carts.models import Cart
from users.models import User
from django.shortcuts import get_object_or_404
from carts.permissions import IsCartOwner
from .permissions import IsOrdersOwner, IsOrderProductOwner, IsSalesSummaryOwner
from drf_spectacular.utils import extend_schema
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.utils.translation import gettext as _
from purchase_orders.models import PurchaseOrders


@extend_schema(
    tags=["Carts"],
)
class PurchaseOrderCreateView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCartOwner]
    queryset = PurchaseOrders
    serializer_class = PurchaseOrdersCreateSerializer

    def perform_create(self, serializer):
        cart_exists = get_object_or_404(Cart, pk=self.kwargs.get("cart_id"))
        serializer.save(user=self.request.user, cart_id=self.kwargs.get("cart_id"))


@extend_schema(
    tags=["Orders"],
)
class PurchaseOrderListClientView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOrdersOwner]
    serializer_class = PurchaseOrdersListClientSerializer

    def get_queryset(self):
        client_id = self.kwargs.get("user_id")
        order = get_object_or_404(User, pk=client_id)
        if self.request.path.__contains__("seller"):
            return PurchaseOrders.objects.filter(seller_id=client_id).order_by(
                "updated_at"
            )
        return PurchaseOrders.objects.filter(user_id=client_id).order_by("updated_at")


@extend_schema(
    tags=["Orders"],
)
class PurchaseOrderDetailView(RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOrderProductOwner]
    queryset = PurchaseOrders.objects.all()
    serializer_class = PurchaseOrdersUpdateSerializer


@extend_schema(
    tags=["Orders"],
    description="Retorna um resumo em PDF das vendas.",
    responses={
        200: {
            "description": "Arquivo PDF com o resumo das vendas.",
            "content": {
                "application/pdf": {
                    "schema": {
                        "type": "string",
                        "format": "binary",
                    },
                },
            },
        },
    },
)
class PurchaseOrderListGeneratePdfPdfView(RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSalesSummaryOwner]

    def get(self, request, *args, **kwargs):
        seller = User.objects.filter(pk=request.user.id)

        list_orders = PurchaseOrders.objects.filter(seller_id=request.user.id).order_by(
            "updated_at"
        )

        total_in_sales = 0
        for order in list_orders:
            total_in_sales += order.price

        # cria o arquivo PDF
        pdf_file = BytesIO()
        pdf = canvas.Canvas(pdf_file)

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(250, 780, "Resumo de vendas")
        pdf.setFont("Helvetica", 14)

        pdf.drawString(
            100, 740, f"Vendedor: {seller[0].first_name} {seller[0].last_name}"
        )
        pdf.drawString(100, 720, f"Email: {seller[0].email}")
        pdf.drawString(
            100, 700, f"Quantidade de pedidos vendidos: {list_orders.count()}"
        )
        pdf.drawString(100, 680, f"Valor total em vendas: R$ {total_in_sales}")

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(100, 640, f"Lista de pedidos vendidos:")
        pdf.setFont("Helvetica", 14)

        keys_order_in_pdf = [
            "id",
            "status",
            "price",
            "quantity_items",
            "created_at",
            "updated_at",
        ]

        # desenha o dicionário de orders no PDF
        y = 600
        pages_pdf = 1
        for index, order in enumerate(list_orders):
            pdf.drawString(100, y, f"Pedido: {index+1}")
            y -= 20
            for key, value in order.__dict__.items():
                if key in keys_order_in_pdf:
                    text = "{}: {}".format(key, value)
                    pdf.drawString(100, y, text)
                    y -= 20
                    # verifica se a próxima linha cabe na página atual
                    if y <= 50:
                        pdf.setFont("Helvetica-Bold", 14)
                        pdf.drawString(500, y, f"p.{pages_pdf}")
                        pdf.setFont("Helvetica", 14)
                        pages_pdf += 1
                        # se não couber, chama o método showPage() para criar uma nova página
                        pdf.showPage()
                        y = 750  # define a posição vertical para o topo da nova página
                        pdf.setFont("Helvetica-Bold", 14)
                        pdf.drawString(200, y, "Continuação do resumo das vendas:")
                        pdf.setFont("Helvetica", 14)
                        y -= 40  # atualiza a posição vertical para a próxima linha na nova página
            pdf.drawString(100, y, "--------------------------------------------")
            y -= 20
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(500, 40, f"p.{pages_pdf}")
        pdf.setFont("Helvetica", 14)
        pdf.showPage()
        pdf.save()

        # retorna o arquivo PDF como uma resposta HTTP
        response = HttpResponse(pdf_file.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = "filename=sales_summary.pdf"
        return response
