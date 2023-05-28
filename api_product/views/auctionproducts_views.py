from django.db.models import Max

from api_base.views import BaseAdminModelView
from api_product.services import AuctionProductService
from api_product.serializers import AuctionProductRequestSerializers, AuctionProductResponseSerializers, ProductResponseSerializer
from api_product.models import AuctionProduct, Products
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class AuctionProductViewSet(BaseAdminModelView):
    scopes = {
        "create": "user",
        "retrieve": "user",
        "get_list_auction_of_user": "user",
        "get_list_auction_of_art": "anonymous,user",
    }
    serializer_class = AuctionProductResponseSerializers
    queryset = AuctionProduct.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        serializers = AuctionProductRequestSerializers(data=data)
        serializers.is_valid(raise_exception=True)

        message, is_valid = AuctionProductService.create(request=request, data=serializers.validated_data)

        return Response(data=message, status=status.HTTP_201_CREATED if is_valid else status.HTTP_400_BAD_REQUEST)

    @action(methods=["GET"], detail=False, name="get_list_auction_of_user")
    def get_list_auction_of_user(self, request, *args, **kwargs):
        queries = AuctionProduct.objects.filter(user=request.user).values("product").annotate(price_max=Max('auction_price')).order_by()
        list_product = []
        for query in queries:
            serializer = ProductResponseSerializer(instance=Products.objects.get(pk=query.get('product').hex), many=False)
            list_product.append({"product": serializer.data, "price_max": query.get("price_max")})
        return Response(data=list_product, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=True, name="get_list_auction_of_art")
    def get_list_auction_of_art(self, request, pk, *args, **kwargs):
        queries = AuctionProduct.objects.filter(product=pk)
        if queries.exists():
            many = True
            if len(queries) == 1:
                queries = queries.first()
                many = False
            serializer = AuctionProductResponseSerializers(instance=queries, many=many)
            return Response(data=serializer.data if many else [serializer.data], status=status.HTTP_200_OK)
        return Response(data=[], status=status.HTTP_200_OK)

    @action(methods=["PUT"], detail=True, name="approve_auction")
    def approve_auction(self, request, pk, *args, **kwargs):
        message, is_valid = AuctionProductService.approve_auction(pk=pk)
        return Response(data=message, status=status.HTTP_200_OK if is_valid else status.HTTP_400_BAD_REQUEST)
