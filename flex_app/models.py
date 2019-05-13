from django.db import models


class FlexPostModel(models.Model):
    post_id = models.AutoField(primary_key=True)

    author = models.ForeignKey('account_app.UserModel', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    pawn_post = models.ForeignKey('pawn_app.PawnPostModel', on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=1024)

    like = models.IntegerField(default=0)


class FlexCommentModel(models.Model):
    comment_id = models.AutoField(primary_key=True)

    flex_post = models.ForeignKey(FlexPostModel, on_delete=models.CASCADE)
    author = models.ForeignKey('account_app.UserModel', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    content = models.CharField(max_length=1024)


class FlexPhotoModel(models.Model):
    image_id = models.AutoField(primary_key=True)
    flex_post = models.ForeignKey(FlexPostModel, on_delete=models.CASCADE)
    photo = models.ImageField()


class FlexPostLikeModel(models.Model):
    flex_post = models.ForeignKey(FlexPostModel, on_delete=models.CASCADE)
    user = models.ForeignKey('account_app.UserModel', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('flex_post', 'user',)
