from django.contrib.auth import get_user_model
from rest_framework import serializers

from pawn_app.models import PawnPostModel
from . import models


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
    content = serializers.CharField(
        max_length=1024,
        write_only=True,
    )


class FlexPostRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FlexPostModel
        fields = '__all__'

    comments = serializers.JSONField(read_only=True)
    photos = serializers.ListField(
        child=serializers.ImageField(),
        read_only=True,
    )


class FlexPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FlexPhotoModel
        fields = '__all__'

    flex_post = serializers.PrimaryKeyRelatedField(queryset=models.FlexPostModel.objects.all())
