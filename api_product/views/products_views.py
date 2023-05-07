from django.shortcuts import render
from api_base.views import BaseAdminModelView
from api_product.serializers import ProductRequestSerializer, ProductResponseSerializer
from api_product.services import ProductService
from rest_framework.response import Response
from rest_framework import status
from api_product.models import Products, ImageProduct
from rest_framework.decorators import action
from api_base.services import BaseService



# Create your views here.

class ProductViewSet(BaseAdminModelView):
    scopes = {
        "list": "anonymous",
    }
    queryset = Products.objects.all()
    serializer_class = ProductResponseSerializer

    def list(self, request, *args, **kwargs):
        data = ProductService().list(request)
        print(data)
        return Response(data=data, status=status.HTTP_200_OK)

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
        product_serializer = ProductRequestSerializer(data=data)
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
        message = "successfully" if objs is not None else "file is not valid"
        return Response(data=message, status=status.HTTP_200_OK if objs is not None else status.HTTP_400_BAD_REQUEST)
