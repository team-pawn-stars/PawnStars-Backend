from rest_framework import serializers

from . import models


class BuyerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = ('username', 'password', 'phone', 'name')

    def create(self, validated_data):
        user = models.UserModel(
            username=validated_data['username'],
            phone=validated_data['phone'],
            name=validated_data['name']
        )
        user.set_password(validated_data['password'])

        user.save()
        return user


class SellerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = ('username', 'password', 'phone', 'name', 'longitude', 'latitude')

    def create(self, validated_data):
        user = models.UserModel(
            username=validated_data['username'],
            phone=validated_data['phone'],
            name=validated_data['name'],
            is_seller=True,

            longitude=validated_data['longitude'],
            latitude=validated_data['latitude'],
        )
        user.set_password(validated_data['password'])

        user.save()
        return user


class PawnPostSerializer(serializers.ModelSerializer):
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
        queryset=models.UserModel.objects.all()
    )

    history = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(
            queryset=models.PawnHistoryModel.objects.all()
        ),
        read_only=True
    )


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
