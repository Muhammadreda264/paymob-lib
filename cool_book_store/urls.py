from rest_framework.routers import DefaultRouter
from books.views import BookViewSet


# Initialize the DefaultRouter
router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

