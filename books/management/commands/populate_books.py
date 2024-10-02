import random

from django.core.management.base import BaseCommand
from faker import Faker

from books.models import Book


class Command(BaseCommand):
    help = "Populate the Book model with fake data"

    def add_arguments(self, parser):
        # Adding an optional argument for the number of books
        parser.add_argument(
            "--num-books",
            type=int,
            default=10,
            help="Number of fake books to create (default is 10)",
        )

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Get the number of books from the command-line argument
        num_books = kwargs["num_books"]

        for _ in range(num_books):
            title = fake.catch_phrase()
            author = fake.name()
            publishing_date = fake.date()
            category = random.choice(["Fiction", "Non-Fiction", "Science", "History"])
            url = fake.url()
            average_rating = round(random.uniform(1, 5), 2)

            Book.objects.create(
                title=title,
                author=author,
                publishing_date=publishing_date,
                category=category,
                url=url,
                average_rating=average_rating,
            )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully added {num_books} fake books.")
        )
