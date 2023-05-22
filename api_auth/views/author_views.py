from api_base.views import BaseAdminModelView
from api_auth.serializers import AuthorResponseSerializer
from api_auth.models import Author, Role
from rest_framework.response import Response
from rest_framework import status

class AuthorModelViewSet(BaseAdminModelView):
    serializer_class = AuthorResponseSerializer
    queryset = Author.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        data["role"] = Role.objects.filter(name="author").first()
        serializer = AuthorResponseSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data="Create Author success", status=status.HTTP_201_CREATED)
        return Response(data="Data is not valid", status=status.HTTP_400_BAD_REQUEST)



