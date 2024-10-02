# reviews/management/commands/populate_reviews.py

import random
from django.core.management.base import BaseCommand
from faker import Faker
from reviews.models import Review
from django.contrib.auth.models import User
from books.models import Book

class Command(BaseCommand):
    help = 'Populate the Review model with fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        users = User.objects.all()  # Fetch all users to assign as reviewers
        books = Book.objects.all()  # Fetch all books to assign reviews
        #TODO: Make ths a param to the script
        for _ in range(10):
            review = Review(
                book=random.choice(books),  # Randomly select a book
                reviewer=random.choice(users),  # Randomly select a user as reviewer
                rating=random.randint(1, 5),  # Random rating between 1 and 5
                comment=fake.text(max_nb_chars=200)  # Fake comment text
            )
            review.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully created review for {review.book.title}'))
