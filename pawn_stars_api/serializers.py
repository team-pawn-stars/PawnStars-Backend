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
