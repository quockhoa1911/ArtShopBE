from rest_framework import serializers
from api_auth.models import Expert, Role


class ExpertResponseSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())

    class Meta:
        model = Expert
        fields = ["id", "name", "work_from", "role", "birthday"]
