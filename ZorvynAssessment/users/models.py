from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Application user model with role-based authorization metadata."""

    class Role(models.TextChoices):
        VIEWER = 'VIEWER', 'Viewer'
        ANALYST = 'ANALYST', 'Analyst'
        ADMIN = 'ADMIN', 'Admin'

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.VIEWER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        """Return a readable identifier for admin and logs."""
        return self.username
