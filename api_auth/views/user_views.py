from api_base.views import BaseModelView, BaseAdminModelView
from api_auth.serializers import UserRegisterSerializers, UserLoginSerialiers, UserResponseSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from api_auth.services import UserServices
from api_auth.models import User, Role
from django.shortcuts import get_object_or_404


# Create your views here.

class UserModelViewSet(BaseAdminModelView):
    scopes = {
        "create": "anonymous",
        "login": "anonymous",
        "me": "user",
        # "update_profile": "user"
    }
    serializer_class = UserResponseSerializers
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        role = Role.objects.get(name="user")
        user = User.objects.filter(role=role)
        if len(user) > 1:
            many = True
        if len(user) == 1:
            many = False
            user = user.first()
        serializer = UserResponseSerializers(instance=user, many=many)
        return Response(data=[serializer.data] if not many else serializer.data,
                        status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        role = Role.objects.get(name="user")
        data["role"] = role.id.hex
        serializer = UserRegisterSerializers(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data="Register success", status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False, name="login")
    def login(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerialiers(data=data)
        serializer.is_valid(raise_exception=True)
        res = UserServices.login(serializer.validated_data)
        return Response(data=res, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, name="me")
    def me(self, request, *args, **kwargs):
        id = request.user.id
        user = get_object_or_404(User, pk=id)
        serializer = UserResponseSerializers(instance=user, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    # @action(methods=['POST'], detail=False, url_path="me/update_profile", name="update_profile")
    # def update_profile(self, request, *args, **kwargs):
    #     user = request.user
    #     context = {"id": user.id.hex}
    #     serializer = UserUpdateSerializer(data=request.data, context=context)
    #     serializer.is_valid(raise_exception=True)
    #     user.name = serializer.validated_data["name"]
    #     user.phone_number = serializer.validated_data["phone_number"]
    #     user.save()
    #     return Response(data="Update success", status=status.HTTP_200_OK)

    @action(methods=["PUT"], detail=True, name="change_active")
    def change_active(self, request, pk, *args, **kwargs):
        user = User.objects.get(pk=pk)
        user.is_active = not user.is_active
        user.save()
        serializer = UserResponseSerializers(instance=user, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, name="delete_user")
    def delete_user(self, request, *args, **kwargs):
        email = request.data['email']
        user = User.objects.get(email=email)
        user.delete()
        return Response(data="Del user", status=status.HTTP_204_NO_CONTENT)
