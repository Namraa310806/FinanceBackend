from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
    ValidationError,
)
from rest_framework.response import Response
from rest_framework.views import exception_handler


def _normalize_errors(data):
    """Recursively coerce error payloads into JSON-serializable primitives."""
    if isinstance(data, dict):
        return {key: _normalize_errors(value) for key, value in data.items()}
    if isinstance(data, list):
        return [_normalize_errors(item) for item in data]
    return str(data)


def custom_exception_handler(exc, _context):
    """Convert DRF exceptions into the standardized error response envelope."""
    response = exception_handler(exc, _context)

    if response is None:
        return Response(
            {
                'status': 'error',
                'message': 'An unexpected error occurred.',
                'errors': {'detail': 'Internal server error.'},
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    message = 'Request failed.'
    if isinstance(exc, ValidationError):
        message = 'Validation failed.'
    elif isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        message = 'Authentication failed.'
    elif isinstance(exc, (PermissionDenied, DjangoPermissionDenied)):
        message = 'You do not have permission to perform this action.'
    elif isinstance(exc, Http404):
        message = 'Requested resource was not found.'

    response.data = {
        'status': 'error',
        'message': message,
        'errors': _normalize_errors(response.data),
    }
    return response
