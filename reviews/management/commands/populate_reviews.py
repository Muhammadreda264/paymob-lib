import random

from books.models import Book
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker

from reviews.models import Review


class Command(BaseCommand):
    help = "Populate the Review model with fake data"

    def add_arguments(self, parser):
        # Adding an optional argument for the number of reviews
        parser.add_argument(
            "--num-reviews",
            type=int,
            default=10,
            help="Number of fake reviews to create (default is 10)",
        )

    def handle(self, *args, **kwargs):
        fake = Faker()
        books = Book.objects.all()  # Fetch all books to assign reviews
        num_books = books.count()

        if num_books == 0:
            self.stdout.write(
                self.style.ERROR("No books found in the database. Exiting.")
            )
            return

        # Get the number of reviews from the command-line argument
        num_reviews = kwargs["num_reviews"]

        # Calculate the minimum number of users needed based on the number of reviews and books
        users_needed = (num_reviews // num_books) + 1

        # Check how many users exist
        existing_users = User.objects.count()

        # Create additional users if needed
        if existing_users < users_needed:
            users_to_create = users_needed - existing_users
            self.stdout.write(
                self.style.WARNING(
                    f"Creating {users_to_create} additional users to meet the review demand."
                )
            )

            for _ in range(users_to_create):
                username = fake.unique.user_name()
                email = fake.unique.email()
                password = fake.password()
                User.objects.create_user(
                    username=username, email=email, password=password
                )
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created {users_to_create} users.")
            )

        # Fetch all users again after creation
        users = User.objects.all()

        reviews_created = 0
        for _ in range(num_reviews):
            book = random.choice(books)  # Randomly select a book
            user = random.choice(users)  # Randomly select a user as reviewer

            # Check if this user has already reviewed the selected book
            if Review.objects.filter(book=book, reviewer=user).exists():
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipping: {user.username} has already reviewed {book.title}"
                    )
                )
                continue  # Skip to the next iteration if a review already exists

            # Create and save the review if no review exists for this user-book pair
            review = Review(
                book=book,
                reviewer=user,
                rating=random.randint(1, 5),  # Random rating between 1 and 5
                comment=fake.text(max_nb_chars=200),  # Fake comment text
            )
            review.save()
            reviews_created += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created review for {review.book.title} by {review.reviewer.username}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(f"Total reviews created: {reviews_created}")
        )
