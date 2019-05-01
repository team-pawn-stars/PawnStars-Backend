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

    price = serializers.CharField(max_length=256)
    like = serializers.CharField(max_length=256)
    author = serializers.CharField(max_length=128)
    photo = serializers.ImageField(default='default.jpg')


class PawnPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PawnPhotoModel
        fields = '__all__'
