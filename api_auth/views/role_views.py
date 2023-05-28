from api_auth.models import Role
from api_auth.serializers import RoleResponseSerializer
from api_base.views import BaseAdminModelView


class RoleModelViewSet(BaseAdminModelView):
    serializer_class = RoleResponseSerializer
    queryset = Role.objects.all()
