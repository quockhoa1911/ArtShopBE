from api_base.views import BaseModelView
from api_auth.serializers import UserRegisterSerializers, UserLoginSerialiers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from api_auth.services import UserServices


# Create your views here.

class UserModelViewSet(BaseModelView):

    def create(self, request, *args, **kwargs):
        data = request.data
        serialier = UserRegisterSerializers(data=data)
        serialier.is_valid(raise_exception=True)
        serialier.save()
        return Response(data="Register success", status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False, name="login")
    def login(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerialiers(data=data)
        serializer.is_valid(raise_exception=True)
        res = UserServices.login(serializer.validated_data)
        return Response(data=res, status=status.HTTP_200_OK)
