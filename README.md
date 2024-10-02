
# Cool Book Store

## Overview
Cool Book Store is a Django-based application that allows users to browse books, read reviews, and submit their own reviews. The app uses JWT (JSON Web Tokens) for authentication, ensuring secure access to user-related actions.

## Features
- Users can sign up and create an account.
- View a list of available books.
- View details and contents of each book.
- Read reviews from other users.
- Submit a review for a book (one review per book per user).
- Users can edit or delete their own reviews.
- Both authenticated users and unauthenticated visitors can view books and reviews.

## Prerequisites
- Python 3.x
- Django
- Django REST Framework
- PostgreSQL (or any other database you prefer)

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Muhammadreda264/paymob-lib/
cd cool-book-store
```

### 2. Set Up a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up the Database
1. Update your database settings in `settings.py`.
2. Run migrations:
   ```bash
   python manage.py migrate
   ```

### 5. Create a Superuser
To access the Django admin panel:
```bash
python manage.py createsuperuser
```

### 6. Run the Development Server
```bash
python manage.py runserver
```
Now you can access the app at `http://127.0.0.1:8000/`.


## Populating Books and Reviews

### 1. Populating Books
To populate the database with pre-defined books, you can use the Django admin panel or create a management command. 
- **Using Admin Panel**: Log in to the admin panel (`/admin`) and add books manually.
- **Using Shell Command**:
```bash
python manage.py populate_books --num-books 10  # Adjust the number as needed
```

### 2. Populating Reviews
Similarly, you can populate reviews using a management command:
```bash
python manage.py populate_reviews --num-reviews 20  # Adjust the number as needed
```
## Running with Docker
### 1. Build and Run Docker Containers

```bash
docker-compose up --build
```
### 2. Migrate the Database

To apply migrations inside the Docker container:
```bash
docker-compose exec web python manage.py migrate
```
### Create a Superuser

You can create a superuser within the Docker container by running:

```bash
docker-compose exec web python manage.py createsuperuser
```
### Access the Application

Now you can access the app at http://localhost:8000/.
### Populating Books with docker

```bash
    sudo docker-compose exec web python manage.py populate_books --num-books 10  # Adjust the number as needed
```
### Populating Reviews
```bash
sudo docker-compose exec web python manage.py populate_reviews --num-reviews 20  # Adjust the number as needed
```

### 3. JWT Authentication
Users can register and log in to obtain a JWT token:
- **Register**: POST request to `/api/auth/register/` with `username` and `password`.
- **Login**: POST request to `/api/auth/login/` with `username` and `password` to receive the token.

Include the token in the `Authorization` header for any requests that require authentication.

## API Endpoints
- `GET /api/books/` - List all available books.
- `GET /api/books/<book_id>/` - Get details of a specific book.
- `GET /api/books/<book_id>/reviews/` - Get reviews for a specific book.
- `POST /api/books/<book_id>/reviews/` - Submit a review for a specific book (authenticated users only).
- `PUT /api/reviews/<review_id>/` - Edit a review (authenticated users only).
- `DELETE /api/reviews/<review_id>/` - Delete a review (authenticated users only).


