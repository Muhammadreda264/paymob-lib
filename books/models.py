from django.db import models
from django.db.models import Avg
from datetime import date

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    publishing_date = models.DateField()
    category = models.CharField(max_length=50)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)  # Cached average rating

    def update_average_rating(self):
        """
        Recalculate and update the average rating based on related reviews.
        """
        reviews = self.reviews.all()
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0.00
        self.average_rating = round(avg_rating, 2)
        self.save()

    def __str__(self):
        return self.title
