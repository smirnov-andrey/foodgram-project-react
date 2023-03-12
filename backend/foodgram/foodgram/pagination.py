from rest_framework.pagination import PageNumberPagination


class CustomLimitPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'limit'
