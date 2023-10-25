.. start-no-pypi
.. image:: https://github.com/labd/django-cognito-jwt/workflows/Python%20Tests/badge.svg
    :target: https://github.com/labd/django-cognito-jwt/workflows/Python%20Tests/

.. image:: http://codecov.io/github/LabD/django-cognito-jwt/coverage.svg?branch=master
    :target: http://codecov.io/github/LabD/django-cognito-jwt?branch=master

.. image:: https://img.shields.io/pypi/v/django-cognito-jwt.svg
    :target: https://pypi.python.org/pypi/django-cognito-jwt/

.. image:: https://readthedocs.org/projects/django-cognito-jwt/badge/?version=latest
    :target: https://django-cognito-jwt.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. end-no-pypi


Django Cognito JWT
==================

An Authentication backend for Django Rest Framework for AWS Cognito JWT tokens


Installation
============

.. code-block:: shell

   pip install django-cognito-jwt

Usage
=====

Add the following lines to your Django ``settings.py`` file:

.. code-block:: python

    COGNITO_AWS_REGION = '<aws region>' # 'eu-central-1'
    COGNITO_USER_POOL = '<user pool>'   # 'eu-central-1_xYzaq'
    COGNITO_AUDIENCE = '<client id>'

(Optional) If you want to cache the Cognito public keys between requests you can
enable the ``COGNITO_PUBLIC_KEYS_CACHING_ENABLED`` setting (it only works if you
have the Django ``CACHES`` setup to anything other than the dummy backend).

.. code-block:: python

    COGNITO_PUBLIC_KEYS_CACHING_ENABLED = True
    COGNITO_PUBLIC_KEYS_CACHING_TIMEOUT = 60*60*24  # 24h caching, default is 300s

Also update the rest framework settings to use the correct authentication backend:

.. code-block:: python

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            ...
            'django_cognito_jwt.JSONWebTokenAuthentication',
            ...
        ],
        ...
     }



Be sure you are passing the ID Token JWT from Cognito as the authentication header.
Using the Access Token will work for authentication only but we're unable to use the `get_or_create_for_cognito` method with the Access Token.


(Optional) If you want to use a different user model then the default DJANGO_USER_MODEL
you can use the ``COGNITO_USER_MODEL`` setting.

.. code-block:: python

	COGNITO_USER_MODEL = "myproject.AppUser"

The library by default uses id token. To use access token, add the following lines to your Django ``settings.py`` file:

.. code-block:: python

	COGNITO_TOKEN_TYPE = "access"  # {'id', 'access'}, default 'id'


As the payload of access token only contains basic user info, we could obtain further info from the `UserInfo endpoint`.
You need to specify the Cognito domain in the ``settings.py`` file to obtain the user info from the endpoint, as follows:

.. code-block:: python

	COGNITO_DOMAIN = "your-user-pool-domain"  # eg, exampledomain.auth.ap-southeast-1.amazoncognito.com

To use the backend functions, at the DJANGO_USER_MODEL, could define methods as follows:

.. code-block:: python

    class CustomizedUserManager(UserManager):
        def get_user(self, payload):
            cognito_id = payload['sub']
            try:
                return self.get(cognito_id=cognito_id)
            except self.model.DoesNotExist:
                return None

        def create_for_cognito(self, payload):
            """Get any value from `payload` here
            ipdb> pprint(payload)
            {'aud': '159ufjrihgehb67sn373aotli7',
            'auth_time': 1583503962,
            'cognito:username': 'john-rambo',
            'email': 'foggygiga@gmail.com',
            'email_verified': True,
            'event_id': 'd92a99c2-c49e-4312-8a57-c0dccb84f1c3',
            'exp': 1583507562,
            'iat': 1583503962,
            'iss': 'https://cognito-idp.us-west-2.amazonaws.com/us-west-2_flCJaoDig',
            'sub': '2e4790a0-35a4-45d7-b10c-ced79be22e94',
            'token_use': 'id'}
            """
            cognito_id = payload['sub']

            try:
                user = self.create(
                    username= payload["cognito:username"] if payload.get("cognito:username") else payload["username"],
                    cognito_id=cognito_id,
                    email=payload['email'],
                    is_active=True)
            except IntegrityError:
                user = self.get(cognito_id=cognito_id)

            return user