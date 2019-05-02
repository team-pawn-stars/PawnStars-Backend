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


class PawnPostModel(models.Model):
    post_id = models.AutoField(primary_key=True)

    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    category = models.CharField(max_length=32)
    region = models.CharField(max_length=32)
    date = models.DateField(auto_now=True)

    title = models.CharField(max_length=64)
    content = models.CharField(max_length=1024)
    price = models.IntegerField()

    like = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class PawnHistoryModel(models.Model):
    pawn_post = models.ForeignKey(PawnPostModel, on_delete=models.CASCADE)
    date = models.DateField()
    content = models.CharField(max_length=64)


class PawnPhotoModel(models.Model):
    image_id = models.AutoField(primary_key=True)
    pawn_post = models.ForeignKey(PawnPostModel, on_delete=models.CASCADE)
    photo = models.ImageField()
