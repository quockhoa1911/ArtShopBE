from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from api_base.permissions import AdminPermission, UserPermission


# Create your views here.

class BaseUserModelView(ModelViewSet):
    authentication_classes = []
    permission_classes = [UserPermission]


class BaseUserAPIView(APIView):
    authentication_classes = []
    permission_classes = [UserPermission]


class BaseAdminModelView(ModelViewSet):
    authentication_classes = []
    permission_classes = [AdminPermission]


class BaseAdminAPIView(APIView):
    authentication_classes = []
    permission_classes = [AdminPermission]
