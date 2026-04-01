from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination

from finance_dashboard.view_mixins import StandardizedViewSetResponseMixin
from transactions.serializers import TransactionFilterSerializer, TransactionSerializer
from transactions.services.transaction_service import TransactionService
from users.permissions import IsReadOnlyOrAdminWrite


class TransactionPagination(PageNumberPagination):
    """Page-number pagination settings for transaction listing."""

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class TransactionViewSet(StandardizedViewSetResponseMixin, viewsets.ModelViewSet):
    """Transaction API endpoints with filtering, search, and soft-delete behavior."""

    serializer_class = TransactionSerializer
    permission_classes = [IsReadOnlyOrAdminWrite]
    pagination_class = TransactionPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['category', 'notes', 'type']
    success_messages = {
        'list': 'Transactions fetched successfully.',
        'retrieve': 'Transaction fetched successfully.',
        'create': 'Transaction created successfully.',
        'update': 'Transaction updated successfully.',
        'destroy': 'Transaction deleted successfully.',
    }

    def get_queryset(self):
        filters = self._validated_filters()
        return TransactionService.list_for_user(self.request.user, filters)

    def perform_update(self, serializer):
        TransactionService.ensure_mutable(serializer.instance)
        serializer.save()

    def perform_create(self, serializer):
        serializer.instance = TransactionService.create_for_user(
            self.request.user,
            serializer.validated_data,
        )

    def perform_destroy(self, instance):
        TransactionService.soft_delete(instance)

    def _validated_filters(self):
        filter_serializer = TransactionFilterSerializer(data=self.request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        return filter_serializer.validated_data
