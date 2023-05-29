from rest_framework import serializers
from api_product.models import AuctionProduct
from api_product.serializers import ProductResponseSerializer
from api_auth.serializers import UserResponseSerializers


class AuctionProductResponseSerializers(serializers.ModelSerializer):
    product = ProductResponseSerializer(many=False, read_only=True)
    user = UserResponseSerializers(many=False, read_only=True)

    class Meta:
        model = AuctionProduct
        fields = ["id", "product", "user", "is_success", "auction_price", "create_at"]


class AuctionProductRequestSerializers(serializers.Serializer):
    product_id = serializers.UUIDField()
    auction_price = serializers.FloatField()
