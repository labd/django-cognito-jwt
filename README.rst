==================
django-cognito-jwt
==================

An Authentication backend for Django Rest Framework for AWS Cognito JWT tokens

Status
======
.. image:: https://travis-ci.org/LabD/django-cognito-jwt.svg?branch=master
    :target: https://travis-ci.org/LabD/django-cognito-jwt

.. image:: http://codecov.io/github/LabD/django-cognito-jwt/coverage.svg?branch=master
    :target: http://codecov.io/github/LabD/django-cognito-jwt?branch=master

.. image:: https://img.shields.io/pypi/v/django-cognito-jwt.svg
    :target: https://pypi.python.org/pypi/django-cognito-jwt/


Installation
============

.. code-block:: shell

   pip install django-cognito-jwt

Usage
=====

Add the following lines to your Django settings.py file:

.. code-block:: python

    COGNITO_AWS_REGION = '<aws region>' # 'eu-central-1'
    COGNITO_USER_POOL = '<user pool>'   # 'eu-central-1_xYzaq'
    COGNITO_AUDIENCE = '<client id>'    # the App Client Id in your AWS Cognito console
    COGNITO_GET_USER_OR_CREATE_FUNCTION = 'USER_MODEL.get_or_create_for_cognito' # your custom get user function name, it will create a new user if it does not exist
    COGNITO_AUTH_HEADER = 'bearer'      # your custom token header, like 'bearer xxxx.xxxxxxxx.xxxx'

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

And for your application send the request, just set the request header's Authorization property to `bearer xxxx.xxxxxxxx.xxxx`, the `bearer` is what you set in setting.py COGNITO_AUTH_HEADER.
