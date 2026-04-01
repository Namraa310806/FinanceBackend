from rest_framework.exceptions import ValidationError

from transactions.models import Transaction


class TransactionService:
    """Business logic for transaction retrieval and mutation."""

    @staticmethod
    def active_queryset_for_user(user):
        """Return only non-deleted transactions for a specific user."""
        return Transaction.objects.filter(user=user, is_deleted=False)

    @staticmethod
    def list_for_user(user, filters=None):
        """Return user transactions with optional validated filtering."""
        queryset = TransactionService.active_queryset_for_user(user)
        if not filters:
            return queryset

        if filters.get('start_date'):
            queryset = queryset.filter(date__gte=filters['start_date'])
        if filters.get('end_date'):
            queryset = queryset.filter(date__lte=filters['end_date'])
        if filters.get('category'):
            queryset = queryset.filter(category__iexact=filters['category'])
        if filters.get('type'):
            queryset = queryset.filter(type=filters['type'])

        return queryset

    @staticmethod
    def create_for_user(user, validated_data):
        """Create a new transaction for the given user."""
        return Transaction.objects.create(user=user, **validated_data)

    @staticmethod
    def ensure_mutable(transaction):
        """Guard against updates to soft-deleted transaction records."""
        if transaction.is_deleted:
            raise ValidationError({'detail': 'Deleted transactions cannot be updated.'})

    @staticmethod
    def soft_delete(transaction):
        """Soft-delete a transaction instance."""
        transaction.soft_delete()
