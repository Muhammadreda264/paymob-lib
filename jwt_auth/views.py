from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.serializers import ModelSerializer
from drf_spectacular.utils import extend_schema


# Serializer for registering new users
class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user
@extend_schema(tags=['Auth'])
# Registration view
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

@extend_schema(tags=['Auth'])
# JWT token view (override to customize token if needed)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass

@extend_schema(tags=['Auth'])
class CustomTokenRefreshView(TokenRefreshView):
    pass
