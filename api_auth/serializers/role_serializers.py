from rest_framework import serializers
from api_auth.models import Role


class RoleResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']
