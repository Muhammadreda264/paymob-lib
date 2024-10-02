from books.models import Book
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from utils.CustomPageNumberPagination import CustomPageNumberPagination

from .models import Review
from .serializers import ReviewSerializer


@extend_schema(
    tags=["Reviews"],
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
class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling review actions such as listing, retrieving, creating, updating, and deleting reviews.

    This ViewSet provides the standard actions for managing reviews, including the ability to filter reviews
    by book, as well as restrict access to creating, updating, and deleting reviews based on user permissions.

    Attributes:
        queryset (QuerySet): A QuerySet containing all review instances.
        serializer_class (Type[ReviewSerializer]): The serializer class for validating and serializing review data.
        permission_classes (list): Permissions that dictate access to the ViewSet actions.
        pagination_class (Type[CustomPageNumberPagination]): Custom pagination class for handling paginated responses.
        throttle_classes (list): Rate limiting applied to the ViewSet actions.

    Methods:
        get_reviews_for_book(book_id):
            Retrieves reviews for a specific book identified by book_id.

        reviews_for_book_by_id(request, book_id=None):
            List all reviews for a specific book if book_id is provided.

        perform_create(serializer):
            Create a review, ensuring a user can only review a book once.

        update(request, *args, **kwargs):
            Update a review if the logged-in user is the owner.

        destroy(request, *args, **kwargs):
            Delete a review if the logged-in user is the owner.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]  # Allow read-only for unauthenticated users
    pagination_class = CustomPageNumberPagination
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        operation_id="list_reviews_for_book",
        description="Get a list of reviews for a specific book.",
        parameters=[
            OpenApiParameter(
                name="book_id",
                description="ID of the book to get reviews for",
                required=True,
                type=int,
            )
        ],
        responses={
            200: ReviewSerializer(many=True),
            404: {"description": "Book not found"},
        },
    )
    def get_reviews_for_book(self, book_id):
        """Retrieves reviews for a specific book."""
        reviews = self.queryset.filter(book_id=book_id)
        return reviews

    @extend_schema(
        operation_id="list_reviews",
        description="List all reviews, or filter by book ID.",
        parameters=[
            OpenApiParameter(
                name="book_id",
                description="ID of the book to filter reviews by",
                required=False,
                type=int,
            )
        ],
        responses={
            200: ReviewSerializer(many=True),
        },
    )
    def reviews_for_book_by_id(self, request, book_id=None):
        """List all reviews for a specific book if `book_id` is provided."""
        try:
            # Check if the book exists
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        reviews = self.get_reviews_for_book(book_id)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)

    @extend_schema(
        operation_id="create_review",
        description="Create a new review for a book. A user can only review the same book once.",
        request=ReviewSerializer,
        responses={
            201: ReviewSerializer,
            400: {"description": "Bad request or validation error"},
        },
    )
    def perform_create(self, serializer):
        """Create a review, ensuring a user can only review a book once."""
        user = self.request.user
        book = serializer.validated_data["book"]

        # Check if the user has already reviewed the book
        if Review.objects.filter(reviewer=user, book=book).exists():
            raise ValidationError("You have already reviewed this book.")

        # Automatically set the reviewer as the logged-in user
        serializer.save(reviewer=user)

    @extend_schema(
        operation_id="update_review",
        description="Update a review. Only the owner can edit their review.",
        request=ReviewSerializer,
        responses={
            200: ReviewSerializer,
            403: {"description": "Permission denied"},
            404: {"description": "Review not found"},
        },
    )
    def update(self, request, *args, **kwargs):
        """Update a review if the logged-in user is the owner."""
        review = self.get_object()  # Get the review instance

        # Check if the logged-in user is the owner of the review
        if review.reviewer != request.user:
            raise PermissionDenied("You do not have permission to edit this review.")

        return super().update(request, *args, **kwargs)

    @extend_schema(
        operation_id="delete_review",
        description="Delete a review. Only the owner can delete their review.",
        responses={
            204: {"description": "Review deleted"},
            403: {"description": "Permission denied"},
            404: {"description": "Review not found"},
        },
    )
    def destroy(self, request, *args, **kwargs):
        """Delete a review if the logged-in user is the owner."""
        review = self.get_object()  # Get the review instance

        # Check if the logged-in user is the owner of the review
        if review.reviewer != request.user:
            raise PermissionDenied("You do not have permission to delete this review.")

        return super().destroy(request, *args, **kwargs)
