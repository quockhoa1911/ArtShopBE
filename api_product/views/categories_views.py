from api_base.views import BaseAdminModelView
from api_product.serializers import CategoryResponseSerializer
from api_product.models import Category


class CategoriesViewSet(BaseAdminModelView):
    scopes = {
        "list": "anonymous,user",
        "retrieve": "anonymous,user"
    }
    serializer_class = CategoryResponseSerializer
    queryset = Category.objects.all()
