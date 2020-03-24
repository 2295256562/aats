from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            "code": "000000",
            "message": "成功",
            'data': {
                'current_page': self.page.number,
                'next': self.get_next_link(),
                'count': self.page.paginator.count,
                'results': data
            }
        })