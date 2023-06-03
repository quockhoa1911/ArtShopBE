from api_base.views import BaseAdminModelView
from api_auth.serializers import ExpertResponseSerializer
from api_auth.models import Expert, Role
from rest_framework.response import Response
from rest_framework import status


class ExpertModelViewSet(BaseAdminModelView):
    serializer_class = ExpertResponseSerializer
    queryset = Expert.objects.all()

    scopes = {
        "list": "anonymous,user",
        "retrieve": "anonymous,user",
    }

    def create(self, request, *args, **kwargs):
        data = request.data
        data["role"] = Role.objects.filter(name="expert").first().id.hex
        serializer = ExpertResponseSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data="Create expert success", status=status.HTTP_201_CREATED)
        return Response(data="Data is not valid", status=status.HTTP_400_BAD_REQUEST)
