from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class Base_CustomPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            'page': {
                'next': self.page.next_page_number() if self.page.has_next() else None,
                'previous': self.page.previous_page_number() if self.page.has_previous() else None
            },
            'total_all': self.page.paginator.count,
            'total_of_page': len(data),
            'total_page': self.page.paginator.num_pages,
            'data': data
        })
