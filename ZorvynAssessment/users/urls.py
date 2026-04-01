from django.urls import path
from rest_framework.routers import DefaultRouter

from users.views import (
    CurrentUserView,
    LoginView,
    RefreshTokenView,
    RegisterView,
    UserManagementViewSet,
)

router = DefaultRouter()
router.register(r'manage', UserManagementViewSet, basename='user-management')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('me/', CurrentUserView.as_view(), name='me'),
]

urlpatterns += router.urls
