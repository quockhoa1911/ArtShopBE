from api_base.views import BaseAdminModelView
from api_auth.serializers import AuthorResponseSerializer, AuthorRequestSerializer
from api_auth.models import Author, Role
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


class AuthorModelViewSet(BaseAdminModelView):
    serializer_class = AuthorResponseSerializer
    queryset = Author.objects.all()

    scopes = {
        "list": "anonymous,user",
        "retrieve": "anonymous,user",
    }

    def create(self, request, *args, **kwargs):
        data = request.data
        data["role"] = Role.objects.filter(name="author").first().id.hex
        serializer = AuthorRequestSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data="Create Author success", status=status.HTTP_201_CREATED)
        return Response(data="Data is not valid", status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["PUT"], detail=False, name="change_role_for_author")
    def change_role_for_author(self, request, *args, **kwargs):
        queries = self.get_queryset()
        author_role = Role.objects.filter(name="author").first()
        for author in queries:
            author.role = author_role
            author.save()
        return Response(data="Change success", status=status.HTTP_200_OK)

