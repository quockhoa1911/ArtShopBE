import os

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
from datetime import datetime, timedelta
from django.db.models import Q
from itertools import chain
import requests


# Create your views here.

class ProductViewSet(BaseAdminModelView):
    scopes = {
        "list": "anonymous,user",
        "retrieve": "anonymous,user",
        "get_product_of_category": "anonymous,user",
        "get_list_product_expire_auction": "anonymous,user",
        "search_product": "anonymous,user"
    }
    queryset = Products.objects.all()
    serializer_class = ProductResponseSerializer
    pagination_class = Base_CustomPagination

    def list(self, request, *args, **kwargs):
        search = request.GET.get("search", None)
        condition = Q()
        if search:
            condition |= Q(name__icontains=search)
        queries = self.get_queryset().filter(condition)
        if request.user.is_anonymous:
            page = self.paginate_queryset(queries)
            serializers = ProductResponseSerializer(instance=page, many=True)
            return self.get_paginated_response(data=serializers.data)
        else:
            # id category
            url = f"https://tracking.loca.lt/event-tracking/get-popular-category-of-user"
            params = {"userId": "5aac87af-5ac6-42a1-9ea2-b51fbd133d3e"}
            res = ""
            # res = requests.request("GET", url, params=params)
            # data = res.json()
            # count_max = 0
            # category = ""
            # for i in data:
            #     if i["count"] > count_max:
            #         count_max = i["count"]
            #         category = i["value"]
            if request.GET.get("page", None) == 1 and res.status_code == 200:
                filter_condition = Q(category__id="id1") | Q(category_id="id2")
                queries_filter = queries.filter(filter_condition)
                page = self.paginate_queryset(queries)
                if queries_filter.exists():
                    combine_chain = list(chain(queries_filter, queries.exclude(filter_condition)))
                    page = self.paginate_queryset(combine_chain)
                    serializers = ProductResponseSerializer(instance=page, many=True)
                    return self.get_paginated_response(data=serializers.data)

            else:
                page = self.paginate_queryset(queries)
                serializers = ProductResponseSerializer(instance=page, many=True)
                return self.get_paginated_response(data=serializers.data)

            return Response({
                'page': {
                    'next': None,
                    'previous': None
                },
                'total_all': None,
                'total_of_page': None,
                'total_page': 0,
                'data': []
            })

    @action(methods=["GET"], detail=True, name="get_product_of_category")
    def get_product_of_category(self, request, pk, *args, **kwargs):
        data = ProductService().get_product_of_category(id_category=pk)
        return Response(data=data if data is not None else [], status=status.HTTP_200_OK)

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

    @action(methods=["GET"], detail=True, name="search_product")
    def search_product(self, request, pk, *args, **kwargs):
        condition_filer = Q(name__icontains=pk) | Q()
        product_list = Products.objects.filter(condition_filer)
        if product_list.exists():
            page = self.paginate_queryset(product_list)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        return Response({
            'page': {
                'next': None,
                'previous': None
            },
            'total_all': None,
            'total_of_page': None,
            'total_page': 0,
            'data': []
        })

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

    @action(methods=['GET'], detail=False, name='get_list_product_expire_auction')
    def get_list_product_expire_auction(self, request, *args, **kwargs):
        date = datetime.now() + timedelta(days=1)
        queries = self.get_queryset().filter(end_auction__lt=date.date())
        if queries.exists():
            page = self.paginate_queryset(queries)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        return Response({
            'page': {
                'next': None,
                'previous': None
            },
            'total_all': None,
            'total_of_page': None,
            'total_page': 0,
            'data': []
        })
