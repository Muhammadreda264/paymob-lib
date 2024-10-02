from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.

    This serializer handles the serialization and deserialization of Review instances,
    enabling the transformation of Review model instances to JSON format and vice versa.

    Attributes:
        Meta (class): Contains the model and fields that should be included in the serialization.
            - model: Specifies the Review model to serialize.
            - fields: A list of fields to include in the serialized output.
            - read_only_fields: A list of fields that are read-only and cannot be modified through the API.

    Usage:
        This serializer is used to validate input data for creating and updating reviews,
        ensuring that only valid data is accepted.
    """

    class Meta:
        model = Review
        fields = [
            "id",
            "reviewer",
            "book",
            "rating",
            "comment",
            "created_at",
        ]  # Only include these fields for input
        read_only_fields = [
            "id",
            "reviewer",
            "created_at",
        ]  # Ensure these are read-only
