from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy


class UserModel(AbstractUser):
    username = models.CharField(
        gettext_lazy('username'),
        max_length=150,
        primary_key=True,
        help_text=gettext_lazy('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': gettext_lazy("A user with that username already exists."),
        },
    )
    name = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)

    is_seller = models.BooleanField(default=False)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.username
