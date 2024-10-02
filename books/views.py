"""
This module contains viewsets for the Book model.

It provides a read-only interface for retrieving book information, allowing
authenticated users to access all books while permitting unauthenticated users
to read only. The viewset includes pagination support and customizable
parameters for pagination via the OpenAPI schema.
"""

from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from utils.CustomPageNumberPagination import CustomPageNumberPagination

from .models import Book
from .serializers import BookSerializer


@extend_schema(
    tags=["Books"],
    parameters=[
        OpenApiParameter(
            name="page",
            description="Page number for pagination",
            required=False,
            type=int,
        ),
        OpenApiParameter(
            name="page_size",
            description="Number of results per page (max: 100)",
            required=False,
            type=int,
        ),
    ],
)
class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing books.

    This viewset provides a read-only endpoint for retrieving a list of
    books and detailed views of individual books. It supports pagination
    and requires authentication for certain operations while allowing
    public access to view book information.

    Attributes:
        queryset (QuerySet): A queryset of all Book instances.
        serializer_class (Serializer): The serializer for converting
        Book instances to and from JSON.
        permission_classes (list): The list of permission classes to
        determine access rights.
        pagination_class (Pagination): The pagination class for
        controlling how results are paginated.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPageNumberPagination
