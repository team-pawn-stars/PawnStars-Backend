from django.contrib.auth import get_user_model
from rest_framework import viewsets, views

from . import serializers


class BuyerUserView(viewsets.generics.CreateAPIView):
    serializer_class = serializers.BuyerUserSerializer
    model = get_user_model()
