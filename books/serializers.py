"""
This module contains serializers for the Book model.

The BookSerializer handles serialization and deserialization of Book instances,
including formatting the average rating to two decimal places.
"""

from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "publishing_date",
            "category",
            "url",
            "average_rating",
        ]

        def to_representation(self, instance):
            representation = super().to_representation(instance)
            # Format average_rating to have two decimal place
            representation["average_rating"] = format(
                instance.average_rating, ".2f"
            )  # Format as '1.25'
            return representation
