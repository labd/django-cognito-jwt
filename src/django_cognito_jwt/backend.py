import logging

from django.contrib.auth import get_user_model
from django.utils.encoding import smart_text
from django.utils.translation import ugettext as _
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import (
    BaseAuthentication, get_authorization_header)

from django_cognito_jwt.validator import TokenValidator, TokenError

logger = logging.getLogger(__name__)

USER_MODEL = get_user_model()


class JSONWebTokenAuthentication(BaseAuthentication):
    """Token based authentication using the JSON Web Token standard."""

    def __init__(self):
        self._jwt_validator = TokenValidator(
            settings.COGNITO_AWS_REGION,
            settings.COGNITO_USER_POOL,
            settings.COGNITO_AUDIENCE)

        super().__init__()

    def authenticate(self, request):
        """Entrypoint for Django Rest Framework"""
        jwt_token = self.get_jwt_token(request)
        if jwt_token is None:
            return None

        # Authenticate token
        try:
            jwt_payload = self._jwt_validator.validate(jwt_token)
        except TokenError:
            raise exceptions.AuthenticationFailed()

        get_or_create_for_cognito_code = '{function_name}(jwt_payload, request)'.format(
            function_name=settings.COGNITO_GET_USER_OR_CREATE_FUNCTION, jwt_payload=jwt_payload, request=request)

        user = eval(get_or_create_for_cognito_code)
        return (user, jwt_token)

    def get_jwt_token(self, request):
        auth = get_authorization_header(request).split()
        if not auth or smart_text(auth[0].lower()) != settings.COGNITO_AUTH_HEADER:
            return None

        if len(auth) == 1:
            msg = _('Invalid Authorization header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid Authorization header. Credentials string '
                    'should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]

    def authenticate_header(self, request):
        """
        Method required by the DRF in order to return 401 responses for authentication failures, instead of 403.
        More details in https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication.
        """
        return 'Bearer: api'
