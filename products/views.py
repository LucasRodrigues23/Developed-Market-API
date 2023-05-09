from .models import Product
from .serializers import ProductSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import ProductSellerPermission
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


class CustomPaginationProduct(PageNumberPagination):
    page_size = 20


@extend_schema(
    tags=["Products"],
    methods=["GET"],
    description="""Lista todos os produtos cadastrados. É possivel realizar
    filtros na listagem por id, name e categoria do produto. Não é preciso 
    está logado para acessar a rota.
    """,
    parameters=[
        OpenApiParameter(
            name="id",
            description="Id do produto",
            required=False,
            type=OpenApiTypes.UUID,
        ),
        OpenApiParameter(name="name", description="Nome do produto", required=False),
        OpenApiParameter(
            name="category", description="Categoria do produto", required=False
        ),
    ],
)
@extend_schema(
    tags=["Products"],
    methods=["POST"],
    description="""Cadastra um produto, sendo permitido apenas 
    para usuários seller e admin.
    """,
)
class ProductView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [ProductSellerPermission]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPaginationProduct

    def get_queryset(self):
        route_parameter_id = self.request.query_params.get("id")
        route_parameter_name = self.request.query_params.get("name")
        route_parameter_category = self.request.query_params.get("category")

        if route_parameter_id:
            queryset = Product.objects.filter(id__iexact=route_parameter_id)
            return queryset

        if route_parameter_name:
            queryset = Product.objects.filter(name__icontains=route_parameter_name)
            return queryset

        if route_parameter_category:
            queryset = Product.objects.filter(category__iexact=route_parameter_category)
            return queryset

        return super().get_queryset()

    def perform_create(self, serializer):
        return serializer.save(seller=self.request.user)


@extend_schema(
    tags=["Products"],
    description="""Atualiza o estoque do produto, a partir do id do produto,
    informado no parâmetro da rota. Só é possível atualizar o estoque do produto
    pelo vendedor que cadastrou o produto, ou por um usuário admin.
    """,
    methods=["PATCH"],
)
@extend_schema(
    methods=["PUT"],
    exclude=True,
)
class StockProductUpdateView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [ProductSellerPermission]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
