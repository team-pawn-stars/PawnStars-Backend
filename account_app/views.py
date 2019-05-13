from django.contrib.auth import get_user_model
from django.http import HttpRequest, JsonResponse, HttpResponse
from rest_framework import viewsets

from . import serializers


class BuyerUserView(viewsets.generics.CreateAPIView):
    serializer_class = serializers.BuyerUserSerializer
    model = get_user_model()


class SellerUserView(viewsets.generics.CreateAPIView):
    serializer_class = serializers.SellerUserSerializer
    model = get_user_model()


def is_seller(request: HttpRequest, user_id: str):
    if request.method == 'GET':
        user = get_user_model().objects.filter(username=user_id).first()
        return JsonResponse({
            'is_seller': user.is_seller,
        })
    else:
        return HttpResponse(status=405)
