from rest_framework import status
from rest_framework.response import Response


def success_response(message, data=None, status_code=status.HTTP_200_OK):
    """Return a standardized success response payload."""
    return Response(
        {
            'status': 'success',
            'message': message,
            'data': data if data is not None else {},
        },
        status=status_code,
    )
