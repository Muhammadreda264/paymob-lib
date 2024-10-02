from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'  # Name of the query param that allows users to set page size
    max_page_size = 100  # Maximum allowed page size

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total_count': self.page.paginator.count,
            'page_size': self.get_page_size(self.request),
            'results': data
        })
