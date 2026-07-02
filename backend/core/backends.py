from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

User = get_user_model()

class StrictSuperuserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username, password, **kwargs)
        if user and user.is_superuser:
            if user.username != 'amittiwari2236':
                # Alternative superusers are not allowed to authenticate
                raise PermissionDenied("Alternative superuser authentication is disabled.")
        return user
