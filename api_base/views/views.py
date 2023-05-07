from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from api_base.permissions import AdminPermission, UserPermission


# Create your views here.

class ScopeBaseView:
    scopes = {}


class BaseUserModelView(ModelViewSet, ScopeBaseView):
    permission_classes = [UserPermission]


class BaseUserAPIView(APIView, ScopeBaseView):
    permission_classes = [UserPermission]


class BaseAdminModelView(ModelViewSet, ScopeBaseView):
    permission_classes = [AdminPermission]


class BaseAdminAPIView(APIView, ScopeBaseView):
    permission_classes = [AdminPermission]


class BaseModelView(ModelViewSet, ScopeBaseView):
    permission_classes = []


class BaseAPIView(APIView, ScopeBaseView):
    permission_classes = []
