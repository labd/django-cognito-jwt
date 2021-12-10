import logging

from django.apps import apps as django_apps
from django.conf import settings
from django.utils.encoding import force_str
from django.utils.translation import gettext as _
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from django_cognito_jwt.validator import TokenError, TokenValidator

logger = logging.getLogger(__name__)


class JSONWebTokenAuthentication(BaseAuthentication):
    """Token based authentication using the JSON Web Token standard."""

    def authenticate(self, request):
        """Entrypoint for Django Rest Framework"""
        jwt_token = self.get_jwt_token(request)
        if jwt_token is None:
            return None

        # Authenticate token
        try:
            token_validator = self.get_token_validator(request)
            jwt_payload = token_validator.validate(jwt_token)
        except TokenError:
            raise exceptions.AuthenticationFailed()

        USER_MODEL = self.get_user_model()
        user = USER_MODEL.objects.get_or_create_for_cognito(jwt_payload)
        return (user, jwt_token)

    def get_user_model(self):
        user_model = getattr(settings, "COGNITO_USER_MODEL", settings.AUTH_USER_MODEL)
        return django_apps.get_model(user_model, require_ready=False)

    def get_jwt_token(self, request):
        auth = get_authorization_header(request).split()
        if not auth or force_str(auth[0].lower()) != "bearer":
            return None

        if len(auth) == 1:
            msg = _("Invalid Authorization header. No credentials provided.")
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _(
                "Invalid Authorization header. Credentials string "
                "should not contain spaces."
            )
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]

    def get_token_validator(self, request):
        return TokenValidator(
            settings.COGNITO_AWS_REGION,
            settings.COGNITO_USER_POOL,
            settings.COGNITO_AUDIENCE,
        )

    def authenticate_header(self, request):
        """
        Method required by the DRF in order to return 401 responses for authentication failures, instead of 403.
        More details in https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication.
        """
        return "Bearer: api"
