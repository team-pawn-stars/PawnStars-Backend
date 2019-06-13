from django.contrib.auth import get_user_model
from django.http import HttpRequest, JsonResponse, HttpResponse
from rest_framework import viewsets
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from . import serializers


class BuyerUserView(viewsets.generics.CreateAPIView):
    serializer_class = serializers.BuyerUserSerializer
    model = get_user_model()


class SellerUserView(viewsets.generics.CreateAPIView):
    serializer_class = serializers.SellerUserSerializer
    model = get_user_model()


def is_seller(request: HttpRequest):
    if request.method == 'GET':
        user, _ = JSONWebTokenAuthentication().authenticate(request)
        return JsonResponse({
            'is_seller': user.is_seller,
            'name': user.name
        })
    else:
        return HttpResponse(status=405)
