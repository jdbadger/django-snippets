from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.signing import (
    BadSignature,
    SignatureExpired,
    TimestampSigner
)
from django.utils.translation import gettext_lazy as _

from rest_framework import authentication
from rest_framework import exceptions


def get_stateless_auth_token_signer():
    return TimestampSigner(salt='stateless_auth_token')


class StatelessTokenAuthentication(authentication.BaseAuthentication):

    """
    Supports stateless token authentication for users directly or via
    an intermediate model e.g.

    class Application(models.Model):

        ...

        user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name='applications'
        )

        ...

    If using an intermediate model, subclass this backend and override 'model'.

    The maximum age for tokens may be overriden by sublassing this backend and 
    defining 'max_age' in seconds.
    """

    keyword = 'Token'
    model = settings.AUTH_USER_MODEL
    max_age = 3600  # 1hr

    def authenticate(self, request):
        # the method is pretty much lifted straight from DRF's
        # authentication.TokenAuthentication backend class...
        auth = authentication.get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _(
                'Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        auth_failed_msg = "Invalid credentials"

        # validate stateless token
        try:
            signer = get_stateless_auth_token_signer()
            pk = signer.unsign(token, max_age=self.max_age)
        except BadSignature:
            raise exceptions.AuthenticationFailed(auth_failed_msg)
        except SignatureExpired:
            raise exceptions.AuthenticationFailed(auth_failed_msg)

        # retrieve the user associated with the token
        if isinstance(model, settings.AUTH_USER_MODEL):
            try:
                user = model.objects.get(pk=pk, is_active=True)
            except ObjectDoesNotExist:
                raise exceptions.AuthenticationFailed(auth_failed_msg)
            return user, token
        else:
            try:
                model = model.objects.get(pk=pk)
                user = get_user_model().objects.get(id=model.user_id, is_active=True)
            except ObjectDoesNotExist:
                raise exceptions.AuthenticationFailed(auth_failed_msg)
            return user, token
