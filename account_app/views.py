from django.contrib.auth import get_user_model
from rest_framework import viewsets

from . import serializers


class BuyerUserView(viewsets.generics.CreateAPIView):
    serializer_class = serializers.BuyerUserSerializer
    model = get_user_model()


class SellerUserView(viewsets.generics.CreateAPIView):
    serializer_class = serializers.SellerUserSerializer
    model = get_user_model()
