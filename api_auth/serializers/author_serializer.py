from rest_framework import serializers
from api_auth.models import Author, Role


class AuthorRequestSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())

    class Meta:
        model = Author
        fields = ["name", "role", "origin", "birthday"]


class AuthorResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "role", "origin", "birthday"]
        depth = 1
