from api_product.models import Products, Category
from api_auth.models import Author, Expert
from api_product.serializers import ProductResponseSerializer
from api_base.utils import Utils
from django.db.models import  Q


class ProductService:

    def create_or_update_product(self, product: dict, id=None):
        product['category'] = Category.objects.get(pk=product['category'])
        product['author'] = Author.objects.get(pk=product['author'])
        product['slug'] = Utils.no_accent_vietnamese(product.get("name").lower()).replace(" ", "_")
        product['expert'] = Expert.objects.get(pk=product['expert'])
        obj, created = Products.objects.update_or_create(
            id=id if id is not None else None,
            defaults={**product}
        )
        return obj.id

    def list_gather_of_categories(self, request):
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

    def get_product_of_category(self, id_category):
        product_queries = Products.objects.filter(category=id_category)
        if product_queries.exists():
            many = True
            if len(product_queries) == 1:
                product_queries = product_queries.first()
                many = False
            serializer = ProductResponseSerializer(instance=product_queries, many=many)
            return serializer.data
        return None

    def get_limit_object_category(self, model, filter_obj, limit):
        queries_set = model.objects.filter(category=filter_obj).order_by("-create_at")[:limit]
        if len(queries_set) > 0:
            return queries_set
        return []

    def get_suggest_list(self, pk):
        category = Category.objects.filter(product__id=pk)
        if category.exists():
            category = category.first()
            products = Products.objects.filter(Q(category=category) & ~Q(pk=pk)).order_by("-create_at")[:5]
            if products.exists():
                many = True
                if len(products) == 1:
                    many = False
                    products = products.first()
                product_serializer = ProductResponseSerializer(instance=products, many=many)
                return product_serializer.data
        return []


