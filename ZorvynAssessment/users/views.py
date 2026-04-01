from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from finance_dashboard.api_response import success_response
from finance_dashboard.view_mixins import StandardizedViewSetResponseMixin
from users.permissions import IsAdminRole
from users.serializers import (
    AdminUserManagementSerializer,
    LoginTokenObtainPairSerializer,
    RegisterSerializer,
    UserSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """Public endpoint to register a new user account."""

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user_serializer = UserSerializer(serializer.instance)
        return success_response(
            'User registered successfully.',
            user_serializer.data,
            status_code=status.HTTP_201_CREATED,
        )


class LoginView(TokenObtainPairView):
    """Public endpoint to issue JWT access and refresh tokens."""

    permission_classes = [permissions.AllowAny]
    serializer_class = LoginTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return success_response('Login successful.', serializer.validated_data)


class RefreshTokenView(TokenRefreshView):
    """Public endpoint to refresh JWT access token."""

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return success_response('Token refreshed successfully.', serializer.validated_data)


class CurrentUserView(generics.RetrieveAPIView):
    """Authenticated endpoint for the current user's profile."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return success_response('User profile fetched successfully.', serializer.data)

    def get_object(self):
        return self.request.user


class UserManagementViewSet(StandardizedViewSetResponseMixin, viewsets.ModelViewSet):
    """Admin-only CRUD endpoints for user management."""

    queryset = User.objects.all().order_by('-created_at')
    serializer_class = AdminUserManagementSerializer
    permission_classes = [IsAdminRole]
    success_messages = {
        'list': 'Users fetched successfully.',
        'retrieve': 'User fetched successfully.',
        'create': 'User created successfully.',
        'update': 'User updated successfully.',
        'destroy': 'User deleted successfully.',
    }
