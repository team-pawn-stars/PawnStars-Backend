from django.db import models


class PawnPostModel(models.Model):
    post_id = models.AutoField(primary_key=True)

    author = models.ForeignKey('account_app.UserModel', on_delete=models.CASCADE)
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


class PawnPostLikeModel(models.Model):
    pawn_post = models.ForeignKey(PawnPostModel, on_delete=models.CASCADE)
    user = models.ForeignKey('account_app.UserModel', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('pawn_post', 'user',)
