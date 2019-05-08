from django.contrib.auth import get_user_model
from rest_framework import serializers

from . import models


class PawnPostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PawnPostModel
        fields = '__all__'

    price = serializers.CharField(
        max_length=256
    )
    like = serializers.CharField(
        max_length=256,
        default=0,
        read_only=True
    )
    photo = serializers.ImageField(
        allow_null=True,
        read_only=True
    )
    author = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all()
    )


class PawnPostRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PawnPostModel
        fields = '__all__'

    histories = serializers.JSONField(read_only=True)


class PawnHistorySerializer(serializers.Serializer):
    pawn_post = serializers.PrimaryKeyRelatedField(queryset=models.PawnPostModel.objects.all())
    histories = serializers.JSONField()

    def save(self, **kwargs):
        for history in self.validated_data['histories']:
            models.PawnHistoryModel(
                pawn_post=self.validated_data['pawn_post'],
                date=history['date'],
                content=history['content'],
            ).save()


class PawnPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PawnPhotoModel
        fields = '__all__'

    pawn_post = serializers.PrimaryKeyRelatedField(queryset=models.PawnPostModel.objects.all())