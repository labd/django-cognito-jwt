from django.conf.urls import url

from django_cognito_jwt import JSONWebTokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response


@api_view(http_method_names=['GET'])
@authentication_classes((JSONWebTokenAuthentication,))
def sample_view(request):
    return Response({'hello': 'world'})


urlpatterns = [
    url(r'^$', sample_view, name='sample_view'),
]
