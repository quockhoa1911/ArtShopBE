from rest_framework import serializers
from api_auth.models import User
from api_auth.serializers import RoleResponseSerializer
from django.contrib.auth.hashers import make_password


class UserLoginSerialiers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserRegisterSerializers(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    phone_number = serializers.CharField(max_length=10, min_length=10)

    class Meta:
        model = User
        fields = ['email', 'password', 'phone_number']

    def validate_email(self, value):
        user = User.objects.filter(email__iexact=value)
        if user.exists():
            raise serializers.ValidationError("email must be unique")
        return value

    def create(self, validated_data):
        password = validated_data['password']
        validated_data['password'] = make_password(password)
        return super().create(validated_data)


class UserResponseSerializers(serializers.ModelSerializer):
    role = RoleResponseSerializer(many=False, read_only=True)
    password = serializers.HiddenField(default=None)

    class Meta:
        model = User
        fields = ["id", "email", "phone_number", "role", "password"]
