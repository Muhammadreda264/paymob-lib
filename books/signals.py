from django.db.models.signals import post_save
from django.dispatch import receiver
from reviews.models import Review

@receiver(post_save, sender=Review)
def update_book_average_rating(sender, instance, **kwargs):
    """Update the average rating of the book whenever a review is created or updated."""
    instance.book.update_average_rating()
