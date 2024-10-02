import random
from django.core.management.base import BaseCommand
from faker import Faker
from books.models import Book


class Command(BaseCommand):
    help = 'Populate the Book model with fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Number of fake books to create
        num_books = 10

        for _ in range(num_books):
            title = fake.catch_phrase()
            author = fake.name()
            date = fake.date()
            category = random.choice(['Fiction', 'Non-Fiction', 'Science', 'History'])
            url = fake.url()

            Book.objects.create(
                title=title,
                author=author,
                date=date,
                category=category,
                url=url
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully added {num_books} fake books.'))
