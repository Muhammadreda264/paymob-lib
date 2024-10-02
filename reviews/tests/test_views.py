# tests/test_views.py

from books.models import Book
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from reviews.models import Review


class ReviewViewSetTests(APITestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Create a second user for testing purposes
        self.second_user = User.objects.create_user(
            username="seconduser", password="testpassword"
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

    def test_create_review_authenticated(self):
        """Test that an authenticated user can create a review."""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        response = self.client.post(
            reverse("review-list"),
            {"book": self.book.id, "rating": 5, "comment": "Great book!"},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.get().comment, "Great book!")

    def test_create_review_already_exists(self):
        """Test that a user cannot create multiple reviews for the same book."""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        Review.objects.create(
            book=self.book, reviewer=self.user, rating=5, comment="Great book!"
        )

        response = self.client.post(
            reverse("review-list"),
            {"book": self.book.id, "rating": 4, "comment": "Good read!"},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You have already reviewed this book.", str(response.content))

    def test_update_review_authenticated(self):
        """Test that an authenticated user can update their own review."""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        review = Review.objects.create(
            book=self.book, reviewer=self.user, rating=4, comment="Good book!"
        )

        response = self.client.put(
            reverse("review-detail", args=[review.id]),
            {"book": self.book.id, "rating": 5, "comment": "Great book after all!"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        review.refresh_from_db()
        self.assertEqual(review.comment, "Great book after all!")

    def test_update_review_permission_denied(self):
        """Test that a user cannot update someone else's review."""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        review = Review.objects.create(
            book=self.book, reviewer=self.second_user, rating=4, comment="Good book!"
        )

        response = self.client.put(
            reverse("review-detail", args=[review.id]),
            {"book": self.book.id, "rating": 5, "comment": "Not my review!"},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_review_authenticated(self):
        """Test that an authenticated user can delete their own review."""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        review = Review.objects.create(
            book=self.book, reviewer=self.user, rating=4, comment="Good book!"
        )

        response = self.client.delete(reverse("review-detail", args=[review.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 0)

    def test_delete_review_permission_denied(self):
        """Test that a user cannot delete someone else's review."""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        review = Review.objects.create(
            book=self.book, reviewer=self.second_user, rating=4, comment="Good book!"
        )

        response = self.client.delete(reverse("review-detail", args=[review.id]))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_reviews_for_book(self):
        """Test that reviews for a specific book can be retrieved."""
        # Create reviews for the book
        Review.objects.create(
            book=self.book, reviewer=self.user, rating=4, comment="Good book!"
        )
        Review.objects.create(
            book=self.book,
            reviewer=self.second_user,
            rating=5,
            comment="Excellent book!",
        )

        # Make the API request to get reviews for the book
        response = self.client.get(reverse("review-list") + f"?book_id={self.book.id}")

        # Assert that the response status is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the number of results in the 'results' key
        self.assertEqual(
            len(response.data["results"]), 2
        )  # Two reviews for the same book

        # Optionally, check the content of the reviews if needed
        self.assertEqual(response.data["results"][0]["comment"], "Good book!")
        self.assertEqual(response.data["results"][1]["comment"], "Excellent book!")

    def test_get_reviews_for_nonexistent_book(self):
        """Test that trying to get reviews for a nonexistent book returns 404."""
        nonexistent_book_id = 999999999  # Nonexistent book ID
        # Construct the URL using the correct format
        url = reverse(
            "book-reviews", args=[nonexistent_book_id]
        )  # Adjust this based on your URL configuration

        response = self.client.get(url)  # Make the GET request
        # Assert that the response status code is 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_reviews_unauthenticated(self):
        """Test that unauthenticated users can see reviews."""
        # Create a review for testing
        Review.objects.create(
            book=self.book, reviewer=self.user, rating=4, comment="Good book!"
        )

        # Remove the authorization credentials
        self.client.credentials()

        # Get the list of reviews
        response = self.client.get(reverse("review-list"))

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the review is in the response data
        self.assertEqual(
            len(response.data["results"]), 1
        )  # Check length of 'results' key
        self.assertEqual(response.data["results"][0]["comment"], "Good book!")
        self.assertEqual(response.data["results"][0]["rating"], 4)
        self.assertEqual(response.data["results"][0]["book"], self.book.id)
