from rest_framework.pagination import PageNumberPagination


class HymnaryListPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_query_param = "page"
    page_size_query_param = "items_per_page"
    max_page_size = 100
