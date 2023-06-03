from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class Base_CustomPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total_all': self.page.paginator.count,
            'total_of_page': len(data),
            'data': data
        })
