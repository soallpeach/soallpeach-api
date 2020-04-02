from django.contrib.auth.models import User
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from django.utils.translation import gettext_lazy as _


class TokenAuthentication(BaseAuthentication):
    """
    HTTP Basic authentication against username/password.
    """
    www_authenticate_realm = 'api'

    def authenticate(self, request):
        """
        Returns a `User` if a correct username and password have been supplied
        using HTTP Basic authentication.  Otherwise returns `None`.
        """
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No value provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Credentials string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        token = auth[1]
        if token == b'123':
            return User(), None
        raise exceptions.AuthenticationFailed(_('Invalid token'))

    def authenticate_header(self, request):
        return ''
