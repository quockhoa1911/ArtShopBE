from api_product.models import Products, Category
from api_auth.models import Author
from api_product.serializers import ProductResponseSerializer


class ProductService:

    def create_or_update_product(self, product: dict, id=None):
        product['category'] = Category.objects.get(pk=product['category'])
        product['author'] = Author.objects.get(pk=product['author'])
        product['slug'] = product.get("name").lower().replace(" ", "_")
        obj, created = Products.objects.update_or_create(
            id=id if id is not None else None,
            defaults={**product}
        )
        return obj.id

    def list(self, request):
        list_categories = Category.objects.all()
        product = []
        for cate in list_categories:
            queries_product = self.get_limit_object_category(model=Products, filter_obj=cate, limit=3)
            if len(queries_product) > 0:
                many = True
                if len(queries_product) == 1:
                    queries_product = queries_product.first()
                    many = False
                serializer = ProductResponseSerializer(instance=queries_product, many=many)
                product.append([serializer.data] if many is False else serializer.data)

        return product

    def get_limit_object_category(self, model, filter_obj, limit):
        queries_set = model.objects.filter(category=filter_obj).order_by("-create_at")[:limit]
        if len(queries_set) > 0:
            return queries_set
        return []
