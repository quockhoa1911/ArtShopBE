from rest_framework import serializers
from api_auth.models import Author


class AuthorRequestSerializer(serializers.Serializer):

    class Meta:
        model = Author


class AuthorResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "origin", "birthday"]
