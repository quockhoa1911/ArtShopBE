from api_base.views import BaseModelView, BaseAdminModelView
from api_auth.serializers import UserRegisterSerializers, UserLoginSerialiers, UserResponseSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from api_auth.services import UserServices
from api_auth.models import User
from django.shortcuts import get_object_or_404


# Create your views here.

class UserModelViewSet(BaseAdminModelView):
    scopes = {
        "create": "anonymous",
        "login": "anonymous",
        "me": "user"
    }
    serializer_class = UserResponseSerializers
    queryset = User.objects.all()
    def create(self, request, *args, **kwargs):
        data = request.data
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
