from django.contrib.auth.models import AbstractUser
from django.db import models


class UserModel(AbstractUser):
    name = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)

    is_seller = models.BooleanField(default=False)
    longitude = models.FloatField(blank=True)
    latitude = models.FloatField(blank=True)

    def __str__(self):
        return f'{self.username} {self.name}'
