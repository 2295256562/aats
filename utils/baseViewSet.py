from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination, _positive_int, PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from utils.baseresponse import BaseResponse


# class CustomLimitOffsetPagination(LimitOffsetPagination):
#     limit = None
#
#     def get_limit(self, request):
#         if self.limit_query_param:
#             try:
#                 value = request.query_params[self.limit_query_param]
#                 if int(value) == -1:
#                     return int(value)
#                 else:
#                     return _positive_int(
#                         value,
#                         strict=True,
#                         cutoff=self.max_limit
#                     )
#             except (KeyError, ValueError):
#                 pass
#         return self.default_limit
#
#     def paginate_queryset(self, queryset, request, view=None):
#         self.limit = self.get_limit(request)
#         if self.limit == -1:
#             return list(queryset)
#         return super().paginate_queryset(queryset, request, view=None)
#
#     def get_paginated_response(self, data):
#
#         return BaseResponse(data={'count': self.count, 'results': data})



class BaseViewSet(ModelViewSet):
    # pagination_class = CustomLimitOffsetPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return BaseResponse(data=serializer.data, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return BaseResponse(data=serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return BaseResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        """
        put /entity/{pk}/
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return BaseResponse(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        delete /entity/{pk}/
        """
        instance = self.get_object()
        print(instance.__dict__)
        print(type(instance))
        self.perform_destroy(instance)
        return BaseResponse(message='数据删除成功.')


from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from collections import OrderedDict
from rest_framework.response import Response


class LargeResultsSetPagination(LimitOffsetPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000

    def get_paginated_response(self, data):
        code = 0000
        msg = '成功'
        if not data:
            code = 404
            msg = "data not found"

        return Response(OrderedDict([
            ('code', code),
            ('msg', msg),
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data),
        ]))


