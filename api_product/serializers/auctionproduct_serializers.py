from rest_framework import serializers
from api_product.models import AuctionProduct
from api_product.serializers import ProductResponseSerializer
from api_auth.serializers import UserResponseSerializers


class AuctionProductResponseSerializers(serializers.ModelSerializer):
    product = ProductResponseSerializer(many=False, read_only=True)
    user = UserResponseSerializers(many=False, read_only=True)

    class Meta:
        model = AuctionProduct
        fields = ["id", "product", "user", "is_success", "auction_price"]


class AuctionProductRequestSerializers(serializers.Serializer):
    product = serializers.UUIDField()
    auction_price = serializers.CharField()
