from rest_framework import serializers
from api_product.models import Products, ImageProduct
from api_product.serializers import CategoryResponseSerializer
from api_auth.serializers import AuthorResponseSerializer


# class ImageProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ImageProduct
#         fields = ["image"]


class ProductResponseSerializer(serializers.ModelSerializer):
    category = CategoryResponseSerializer(many=False, read_only=True)
    author = AuthorResponseSerializer(many=False, read_only=True)
    images = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="image",
        source="imageproduct"
    )

    class Meta:
        model = Products
        fields = ["id", "name", "category", "author", "slug", "sold", "images", "description", "price", "start_auction", "end_auction",
                  "auction_price"]


class ProductRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    sold = serializers.BooleanField()
    description = serializers.CharField()
    price = serializers.CharField()
    category = serializers.UUIDField()
    author = serializers.UUIDField()
    start_auction = serializers.CharField()
    end_auction = serializers.CharField()
