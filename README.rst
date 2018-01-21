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
    COGNITO_AUDIENCE = '<client id>'    

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
