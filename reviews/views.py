from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Reviews'])
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Allow read-only for unauthenticated users


    def get_reviews_for_book(self, book_id):
        # Filter reviews for the given book
        reviews = self.queryset.filter(book_id=book_id)
        return reviews

    def reviews_for_book_by_id(self, request, book_id=None):
        if book_id is not None:
            reviews = self.get_reviews_for_book(book_id)
            serializer = self.get_serializer(reviews, many=True)
            return Response(serializer.data)
        return super().list(request)

    def perform_create(self, serializer):
        # Automatically set the reviewer as the logged-in user
        serializer.save(reviewer=self.request.user)
