from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ModelSerializer
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

# Serializer for registering new users
class RegisterSerializer(ModelSerializer):
    """
    Serializer for creating new users.

    This serializer handles the registration of new users by validating
    input data and creating a new User instance.

    Attributes:
        username (str): The username of the user, required for registration.
        password (str): The password for the user, write-only.
        email (str): The email address of the user.

    Methods:
        create(validated_data):
            Creates and returns a new User instance based on the validated data.

    Example:
        serializer = RegisterSerializer(data={'username': 'newuser', 'password': 'pass', 'email': 'user@example.com'})
        if serializer.is_valid():
            user = serializer.save()
    """

    class Meta:
        model = User
        fields = ("username", "password", "email")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
        )
        return user


@extend_schema(tags=["Auth"])
# Registration view
class RegisterView(generics.CreateAPIView):
    """
    API view for user registration.

    This view allows unauthenticated users to register by providing their
    username, password, and email. The view uses the RegisterSerializer
    for validation and creating a new User instance.

    Attributes:
        queryset (QuerySet): The queryset containing all User instances.
        permission_classes (tuple): The permission classes for this view, set to AllowAny.
        serializer_class (ModelSerializer): The serializer class used for validating input data.
        throttle_classes (list): The list of throttle classes applied to limit the rate of requests.

    Example:
        POST /api/auth/register/
        {
            "username": "newuser",
            "password": "securepassword",
            "email": "user@example.com"
        }
    """

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    throttle_classes = [AnonRateThrottle]


@extend_schema(tags=["Auth"])
# JWT token view (override to customize token if needed)
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    API view for obtaining JWT tokens.

    This view allows users to obtain access and refresh tokens for authentication.
    It overrides the default TokenObtainPairView to allow customization if needed.

    Example:
        POST /api/auth/token/
        {
            "username": "existinguser",
            "password": "password123"
        }
    """
    pass


@extend_schema(tags=["Auth"])
class CustomTokenRefreshView(TokenRefreshView):
    """
    API view for refreshing JWT tokens.

    This view allows users to refresh their access tokens using the refresh token.
    It overrides the default TokenRefreshView to allow customization if needed.

    Example:
        POST /api/auth/token/refresh/
        {
            "refresh": "your_refresh_token"
        }
    """
    pass
