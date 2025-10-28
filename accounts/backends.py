"""Custom authentication backends for the accounts app."""

from __future__ import annotations

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailBackend(ModelBackend):
    """Authenticate users using the e-mail field as credential."""

    def authenticate(self, request, username=None, password=None, **kwargs):  # type: ignore[override]
        UserModel = get_user_model()
        email = kwargs.get('email', username)

        if email is None or password is None:
            return None

        try:
            user = UserModel.objects.get(email__iexact=email)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
