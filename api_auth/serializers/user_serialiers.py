from rest_framework import serializers
from api_auth.models import User
from api_auth.serializers import RoleResponseSerializer
from django.contrib.auth.hashers import make_password
from api_product.models import AuctionProduct
from django.db.models import Sum
from django.db.models import Q
from django.core.exceptions import ValidationError


class UserLoginSerialiers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserRegisterSerializers(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    phone_number = serializers.CharField(max_length=10, min_length=10)
    name = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'password', 'phone_number', 'name', "role"]

    def validate_email(self, value):
        user = User.objects.filter(email__iexact=value)
        if user.exists():
            raise serializers.ValidationError("email must be unique")
        return value

    def create(self, validated_data):
        password = validated_data['password']
        validated_data['password'] = make_password(password)
        return super().create(validated_data)


# class UserUpdateSerializer(serializers.Serializer):
#     name = serializers.CharField()
#     phone_number = serializers.CharField(max_length=10, min_length=10)
#
#     def validate_name(self, value):
#         user_id = self.context.get("id")
#         user = User.objects.filter(~Q(pk=user_id) & Q(name__iexact=value))
#         if user.exists():
#             raise serializers.ValidationError("name must be unique")
#         return value
#
#     def validate_phone_number(self, value):
#         user_id = self.context.get("id")
#         user = User.objects.filter(~Q(pk=user_id) & Q(phone_number__iexact=value))
#         if user.exists():
#             raise serializers.ValidationError("phone number must be unique")
#         return value
#

class UserResponseSerializers(serializers.ModelSerializer):
    role = RoleResponseSerializer(many=False, read_only=True)
    password = serializers.HiddenField(default=None)

    class Meta:
        model = User
        fields = ["id", "email", "phone_number",
                  "role", "name", "password",
                  "is_active", "visa_card",
                  "is_completed", "address"]

    def to_representation(self, instance):
        instance = super().to_representation(instance)
        queries = AuctionProduct.objects.filter(user=instance.get("id"), is_success=True)
        instance["total_auction_price"] = queries.aggregate(total=Sum('auction_price')).get("total")
        return instance


class UserUpdateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=10, min_length=10)
    name = serializers.CharField()
    address = serializers.CharField()
    visa_card = serializers.CharField(max_length=16)

    def validate_email(self, value):
        id = self.context.get("id", None)

        condition = Q(email__iexact=value)
        if id is not None:
            condition &= ~Q(pk=id)

        user = User.objects.filter(condition)
        if user.exists():
            raise ValidationError("email must be unique")
        return value

    def validate_phone_number(self, value):
        id = self.context.get("id", None)

        condition = Q(phone_number__iexact=value)
        if id is not None:
            condition &= ~Q(pk=id)

        user = User.objects.filter(condition)
        if user.exists():
            raise ValidationError("phone_number must be unique")
        return value
