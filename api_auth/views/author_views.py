from api_base.views import BaseAdminModelView
from api_auth.serializers import AuthorResponseSerializer
from api_auth.models import Author


class AuthorModelViewSet(BaseAdminModelView):
    serializer_class = AuthorResponseSerializer
    queryset = Author.objects.all()
