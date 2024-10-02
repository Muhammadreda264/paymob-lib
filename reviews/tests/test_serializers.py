from books.models import Book
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from reviews.models import Review
from reviews.serializers import ReviewSerializer


class ReviewSerializerTests(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Create a book instance for testing
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            publishing_date="2024-01-01",
            category="Fiction",
            url="http://test.com",
        )

        # Create a review instance for testing
        self.review = Review.objects.create(
            book=self.book, reviewer=self.user, rating=4, comment="Good book!"
        )

    def test_review_serializer_valid_data(self):
        """Test that the serializer accepts valid data."""
        valid_data = {"book": self.book.id, "rating": 5, "comment": "Excellent read!"}

        serializer = ReviewSerializer(data=valid_data, context={"request": self.user})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["rating"], 5)
        self.assertEqual(serializer.validated_data["comment"], "Excellent read!")

    def test_review_serializer_invalid_rating(self):
        """Test that the serializer rejects invalid ratings."""
        invalid_data = {
            "book": self.book.id,
            "rating": 6,  # Invalid rating
            "comment": "Too high rating!",
        }

        serializer = ReviewSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("rating", serializer.errors)

    def test_review_serializer_serialization(self):
        """Test that the serializer can serialize a Review instance."""
        serializer = ReviewSerializer(instance=self.review)
        self.assertEqual(serializer.data["id"], self.review.id)
        self.assertEqual(serializer.data["book"], self.book.id)
        self.assertEqual(serializer.data["reviewer"], self.user.id)
        self.assertEqual(serializer.data["rating"], self.review.rating)
        self.assertEqual(serializer.data["comment"], self.review.comment)
        self.assertIsNotNone(
            serializer.data["created_at"]
        )  # created_at should be populated
