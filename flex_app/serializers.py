from django.contrib.auth import get_user_model
from rest_framework import serializers

from . import models

from pawn_app.models import PawnPostModel


class FlexPostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FlexPostModel
        fields = '__all__'

    post_id = serializers.IntegerField(
        read_only=True,
    )

    author = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
    )

    date = serializers.DateTimeField(
        read_only=True,
    )

    pawn_post = serializers.PrimaryKeyRelatedField(
        queryset=PawnPostModel.objects.all(),
    )

    like = serializers.IntegerField(
        read_only=True,
    )

    photo = serializers.ImageField(
        allow_null=True,
        read_only=True,
    )
