from rest_framework.views import exception_handler
from rest_framework.response import Response
from django_ratelimit.exceptions import Ratelimited

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Handle Rate Limit exceptions
    if isinstance(exc, Ratelimited):
        return Response({'error': 'Rate limit exceeded. Please try again later.'}, status=429)

    return response
