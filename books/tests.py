from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from reviews.models import Review

from books.models import Book
from books.serializers import BookSerializer


class BookViewTests(APITestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Create a book instance
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            publishing_date="2024-01-01",
            category="Fiction",
            url="http://test.com",
            average_rating=4.5,
        )

        # Obtain JWT token for the user
        self.token = self.get_jwt_token()

    def get_jwt_token(self):
        """Helper method to obtain JWT token."""
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "testuser", "password": "testpassword"},
        )
        return response.data["access"]

    def test_get_book_authenticated(self):
        """Test that a book can be retrieved successfully by authenticated users ."""
        # Set the Authorization header with the JWT token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # Get the book details
        response = self.client.get(reverse("book-detail", args=[self.book.id]))

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the returned data is correct
        self.assertEqual(response.data["title"], "Test Book")
        self.assertEqual(response.data["author"], "Test Author")

    def test_get_book_unauthenticated(self):
        """Test that a book can be retrieved successfully by unauthenticated users as well ."""
        # Remove the Authorization header
        self.client.credentials()

        # Attempt to get the book details without authentication
        response = self.client.get(reverse("book-detail", args=[self.book.id]))

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the returned data is correct
        self.assertEqual(response.data["title"], "Test Book")
        self.assertEqual(response.data["author"], "Test Author")


class BookModelTests(TestCase):

    def setUp(self):
        # Create a book instance for testing
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            publishing_date="2024-01-01",
            category="Fiction",
            url="http://test.com",
        )

    def test_create_book(self):
        """Test that a book can be created successfully."""
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.author, "Test Author")
        self.assertEqual(self.book.publishing_date, "2024-01-01")
        self.assertEqual(self.book.category, "Fiction")
        self.assertEqual(self.book.url, "http://test.com")
        self.assertEqual(self.book.average_rating, 0.00)  # Check default average_rating

    def test_update_average_rating(self):
        """Test that average rating is updated correctly based on reviews."""
        # Create related reviews
        user = User.objects.create_user(username="testuser", password="testpassword")
        Review.objects.create(
            book=self.book, reviewer=user, rating=4, comment="Good book!"
        )
        new_user = User.objects.create_user(
            username="another_testuser", password="testpassword"
        )
        Review.objects.create(
            book=self.book, reviewer=new_user, rating=5, comment="Excellent read!"
        )

        # Update the average rating
        self.book.update_average_rating()

        # Check the average rating
        self.assertEqual(self.book.average_rating, 4.50)  # (4 + 5) / 2 = 4.5

    def test_str_method(self):
        """Test the string representation of the Book model."""
        self.assertEqual(str(self.book), "Test Book")


class BookSerializerTests(TestCase):

    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            publishing_date="2024-01-01",
            category="Fiction",
            url="http://test.com",
        )

    def test_serializer_fields(self):
        """Test that the serializer correctly serializes the book instance."""
        serializer = BookSerializer(instance=self.book)
        data = serializer.data

        self.assertEqual(data["id"], self.book.id)
        self.assertEqual(data["title"], self.book.title)
        self.assertEqual(data["author"], self.book.author)
        self.assertEqual(data["publishing_date"], str(self.book.publishing_date))
        self.assertEqual(data["category"], self.book.category)
        self.assertEqual(data["url"], self.book.url)
        self.assertEqual(
            data["average_rating"], format(float(self.book.average_rating), ".2f")
        )  # Compare to formatted average_rating

    def test_serializer_validation(self):
        """Test that the serializer rejects invalid data."""
        invalid_data = {
            "title": "",
            "author": "New Author",
            "publishing_date": "invalid-date",  # Invalid date format
            "category": "Fiction",
            "url": "http://test.com",
        }
        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)
        self.assertIn("publishing_date", serializer.errors)
