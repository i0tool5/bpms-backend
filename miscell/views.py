from rest_framework.decorators import api_view
from rest_framework import (
    permissions,
    exceptions
)


@api_view([*permissions.SAFE_METHODS, 'POST', 'PUT', 'DELETE'])
def handle404(request):
    raise exceptions.NotFound()