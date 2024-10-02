# views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from utils.CustomPageNumberPagination import CustomPageNumberPagination
from .models import Book
from .serializers import BookSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter


@extend_schema(
    tags=['Books'],
    parameters=[
        OpenApiParameter(name='page', description='Page number for pagination', required=False, type=int),
        OpenApiParameter(name='page_size', description='Number of results per page (max: 100)', required=False, type=int)
    ]
)
class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPageNumberPagination