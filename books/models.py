from django.db import models
from django.db.models import Avg


class Book(models.Model):
    """
    Represents a book in the system.

    Attributes:
        title (str): The title of the book, limited to 100 characters.
        author (str): The author of the book, limited to 50 characters.
        publishing_date (date): The date when the book was published.
        category (str): The category of the book, limited to 50 characters.
        url (str): A URL for the book (e.g., a link to its online page).
        created_at (datetime): The timestamp when the book entry was created.
        average_rating (Decimal): The cached average rating of the book,
            represented as a decimal with a maximum of 3 digits and 2 decimal places.
            Defaults to 0.00.

    Methods:
        update_average_rating():
            Recalculates and updates the average rating based on related reviews.

    Example:
        book = Book(title="Example Book", author="Author Name", publishing_date="2024-01-01",
                    category="Fiction", url="http://example.com")
        book.save()
        book.update_average_rating()
    """

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    publishing_date = models.DateField()
    category = models.CharField(max_length=50)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    average_rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=0.00
    )  # Cached average rating

    def update_average_rating(self):
        """
        Recalculate and update the average rating based on related reviews.
        """
        reviews = self.reviews.all()
        avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"] or 0.00
        self.average_rating = round(avg_rating, 2)
        self.save()

    def __str__(self):
        return self.title
