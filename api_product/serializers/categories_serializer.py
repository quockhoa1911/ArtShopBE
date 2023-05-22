from rest_framework import serializers
from api_product.models import Category


class CategoryResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class CategoryRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
