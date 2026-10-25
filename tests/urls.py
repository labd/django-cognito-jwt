from django.urls import re_path
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from django_cognito_jwt import JSONWebTokenAuthentication


@api_view(http_method_names=["GET"])
@authentication_classes((JSONWebTokenAuthentication,))
def sample_view(request):
    return Response({"hello": "world"})


urlpatterns = [re_path(r"^$", sample_view, name="sample_view")]
