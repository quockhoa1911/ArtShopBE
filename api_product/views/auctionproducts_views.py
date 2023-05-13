from api_base.views import BaseAdminModelView
from api_product.services import AuctionProductService
from api_product.serializers import AuctionProductRequestSerializers, AuctionProductResponseSerializers
from api_product.models import AuctionProduct
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class AuctionProductViewSet(BaseAdminModelView):
    scopes = {
        "create": "user",
        "retrieve": "user",
        "get_list_auction_of_user": "user",
    }
    serializer_class = AuctionProductResponseSerializers
    queryset = AuctionProduct.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        serializers = AuctionProductRequestSerializers(data=data)
        serializers.is_valid(raise_exception=True)

        message, is_valid = AuctionProductService.create(request=request, data=serializers.validated_data)

        return Response(data=message, status=status.HTTP_201_CREATED if is_valid else status.HTTP_400_BAD_REQUEST)

    @action(methods=["GET"], detail=True, name="get_list_auction_of_user")
    def get_list_auction_of_user(self, request, pk, *args, **kwargs):
        queries = AuctionProduct.objects.filter(user=pk)
        if queries.exists():
            many = True
            if len(queries) == 1:
                queries = queries.first()
                many = False
            serializer = AuctionProductResponseSerializers(instance=queries, many=many)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data="User hasn't auction", status=status.HTTP_400_BAD_REQUEST)
