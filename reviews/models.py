from books.models import Book  # Import Book model
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Review(models.Model):
    """
    Model representing a review of a book.

    This model associates a review with a specific book and a user who wrote the review.
    Each review includes a rating, a comment, and a timestamp for when it was created.

    Attributes:
        book (ForeignKey): A reference to the Book being reviewed.
        reviewer (ForeignKey): A reference to the User who wrote the review.
        rating (IntegerField): The rating given to the book, restricted to values between 1 and 5.
        comment (TextField): The text of the review.
        created_at (DateTimeField): Timestamp for when the review was created, automatically set on creation.

    Meta:
        constraints (UniqueConstraint): Ensures that a user can only leave one review per book.
    """

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]  # Restrict to values between 1 and 5
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["book", "reviewer"], name="unique_book_reviewer"
            )
        ]

    def __str__(self):
        """
        String representation of the Review instance.

        Returns:
            str: A string representation of the review including the reviewer's name and the book title.
        """
        return f"Review by {self.reviewer} on {self.book.title}"
