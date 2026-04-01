from rest_framework import status

from finance_dashboard.api_response import success_response


class StandardizedViewSetResponseMixin:
    """Wrap common ViewSet responses in the project's success envelope."""

    success_messages = {
        'list': 'Records fetched successfully.',
        'retrieve': 'Record fetched successfully.',
        'create': 'Record created successfully.',
        'update': 'Record updated successfully.',
        'destroy': 'Record deleted successfully.',
    }

    def _message(self, action):
        """Return a configured success message for the current action."""
        return self.success_messages.get(action, 'Request processed successfully.')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            return success_response(
                self._message('list'),
                paginated_response.data,
                status_code=paginated_response.status_code,
            )

        serializer = self.get_serializer(queryset, many=True)
        return success_response(self._message('list'), serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(self._message('retrieve'), serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return success_response(
            self._message('create'),
            serializer.data,
            status_code=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return success_response(self._message('update'), serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(self._message('destroy'), {})
