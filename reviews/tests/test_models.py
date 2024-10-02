from books.models import Book
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from reviews.models import Review


class ReviewModelTests(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Create a second user for testing
        self.second_user = User.objects.create_user(
            username="seconduser", password="testpassword"
        )

        # Create a book instance for testing
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            publishing_date="2024-01-01",
            category="Fiction",
            url="http://test.com",
        )

    def test_create_review(self):
        """Test that a review can be created successfully."""
        review = Review.objects.create(
            book=self.book, reviewer=self.user, rating=4, comment="Good book!"
        )
        self.assertEqual(review.book, self.book)
        self.assertEqual(review.reviewer, self.user)
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.comment, "Good book!")

    def test_review_rating_validation(self):
        """Test that the review rating is validated correctly."""
        with self.assertRaises(ValidationError):
            review = Review(
                book=self.book, reviewer=self.user, rating=0, comment="Bad rating!"
            )
            review.full_clean()  # This should raise a ValidationError

        with self.assertRaises(ValidationError):
            review = Review(
                book=self.book, reviewer=self.user, rating=6, comment="Too high rating!"
            )
            review.full_clean()  # This should raise a ValidationError

    def test_unique_constraint(self):
        """Test that the unique constraint on book and reviewer is enforced."""
        Review.objects.create(
            book=self.book, reviewer=self.user, rating=4, comment="Good book!"
        )

        with self.assertRaises(ValidationError):
            duplicate_review = Review(
                book=self.book, reviewer=self.user, rating=5, comment="Another comment!"
            )
            duplicate_review.full_clean()  # This should raise a ValidationError

        # Create a valid review from another user
        another_review = Review.objects.create(
            book=self.book, reviewer=self.second_user, rating=5, comment="Great book!"
        )
        self.assertIsNotNone(another_review)  # Ensure it is created successfully

    def test_str_method(self):
        """Test the string representation of the Review model."""
        review = Review.objects.create(
            book=self.book, reviewer=self.user, rating=4, comment="Good book!"
        )
        self.assertEqual(str(review), f"Review by {self.user} on {self.book.title}")
