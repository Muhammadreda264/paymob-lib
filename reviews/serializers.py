from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'reviewer','book', 'rating', 'comment', 'created_at']  # Only include these fields for input
        read_only_fields = ['id', 'reviewer', 'created_at']  # Ensure these are read-only
