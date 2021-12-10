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


Example authentication flow
===========================
1) Client sends username and password to DRF using a POST request.
   
2) DRF authenticates it with AWS Cognito using ``AdminInitiateAuth`` (`boto3 <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_initiate_auth>`_) and sends the tokens recived from AWS Congnito back to the client.

3) Client sends request (with the recived ``IdToken`` set as the authentication header) to the API which uses ``django_cognito_jwt.JSONWebTokenAuthentication`` as the ``authentication_classes``

.. code-block:: python
    header = {'Authorization': 'token {}'.format(authentication_result['IdToken'])}
    response = requests.post("http://127.0.0.1:8000/<API with authentication>/", headers=header)    

Note: the `get_or_create_for_cognito` method of the User model needs to be implementated. (refer to: `#11 <https://github.com/labd/django-cognito-jwt/issues/3>`_
