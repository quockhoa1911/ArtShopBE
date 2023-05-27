from django.shortcuts import render
from api_base.views import BaseAdminModelView
from api_product.serializers import ProductRequestSerializer, ProductResponseSerializer
from api_product.services import ProductService
from rest_framework.response import Response
from rest_framework import status
from api_product.models import Products, ImageProduct
from rest_framework.decorators import action
from api_base.services import BaseService
from api_base.pagination import Base_CustomPagination


# Create your views here.

class ProductViewSet(BaseAdminModelView):
    scopes = {
        "list": "anonymous,user",
        "retrieve": "anonymous,user",
        "get_product_of_category": "anonymous,user"
    }
    queryset = Products.objects.all()
    serializer_class = ProductResponseSerializer
    pagination_class = Base_CustomPagination

    def list(self, request, *args, **kwargs):
        queries = self.get_queryset()
        if request.user.is_anonymous:
            page = self.paginate_queryset(queries)
            if page:
                serializers = ProductResponseSerializer(instance=page, many=True)
                return self.get_paginated_response(data=serializers.data)
        else:
            serializers = ProductResponseSerializer(many=True, instance=queries)
        return self.get_paginated_response(serializers.data)

    @action(methods=["GET"], detail=True, name="get_product_of_category")
    def get_product_of_category(self, request, pk, *args, **kwargs):
        data = ProductService().get_product_of_category(id_category=pk)
        status_res = status.HTTP_200_OK
        if data is None:
            data = "Category hasn't product"
            status_res = status.HTTP_400_BAD_REQUEST
        return Response(data=data, status=status_res)

    def create(self, request, *args, **kwargs):
        data = request.data
        product_serializer = ProductRequestSerializer(data=data)
        product_serializer.is_valid(raise_exception=True)
        id_object = ProductService().create_or_update_product(product_serializer.validated_data, None)
        res_data = {
            "message": "Create successfully",
            "id": id_object
        }
        return Response(data=res_data, status=status.HTTP_201_CREATED)

    def update(self, request, pk, *args, **kwargs):
        data = request.data
        context = {"id": pk}
        product_serializer = ProductRequestSerializer(data=data, context=context)
        product_serializer.is_valid(raise_exception=True)
        id_object = ProductService().create_or_update_product(product=data, id=pk)
        res_data = {
            "message": "Update successfully",
            "id": id_object
        }
        return Response(data=res_data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True, name='up_image')
    def up_image(self, request, pk, *args, **kwargs):
        files = request.FILES.getlist("files")
        product = Products.objects.get(pk=pk)
        list_image = []
        for file in files:
            if file:
                file_url = BaseService.upload_file(file)
                list_image.append(ImageProduct(product=product, image=file_url))
        objs = ImageProduct.objects.bulk_create(list_image)
        if not files and not objs:
            product.delete()
        message = "successfully" if objs is not None and files else "file is not valid"
        return Response(data=message,
                        status=status.HTTP_200_OK if objs is not None and files else status.HTTP_400_BAD_REQUEST)

    @action(methods=["DELETE"], detail=False, name="remove_image")
    def remove_image(self, request, *args, **kwargs):
        queries = ImageProduct.objects.all()
        for a in queries:
            a.delete()
        return Response(data="Delete success", status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=True, name='up_image_link')
    def up_image_link(self, request, pk, *args, **kwargs):
        product = Products.objects.get(pk=pk)
        ImageProduct(product=product, image=request.data["link"]).save()
        return Response(data="Save success", status=status.HTTP_201_CREATED)
