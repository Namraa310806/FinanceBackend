from django.conf import settings
from django.utils import timezone
from django.db import models


class Transaction(models.Model):
    """Financial transaction entity owned by a user."""

    class Type(models.TextChoices):
        INCOME = 'INCOME', 'Income'
        EXPENSE = 'EXPENSE', 'Expense'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions',
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=10, choices=Type.choices)
    category = models.CharField(max_length=100)
    date = models.DateField()
    notes = models.TextField(blank=True)
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        """Return a compact text representation for admin and logs."""
        return f'{self.type} {self.amount} - {self.category}'

    def soft_delete(self):
        """Mark a transaction as deleted without removing it from the database."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at'])
