from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response

from const import *
from . import models, serializers


class FlexPostListView(viewsets.generics.ListCreateAPIView):
    serializer_class = serializers.FlexPostListSerializer
    model = models.FlexPostModel

    def get_queryset(self):
        query_params = self.request.query_params
        sort_key = query_params.get(SORT_KEY, NEW)
        page = query_params.get(PAGE, 1)

        query_set = self.model.objects.all()

        if sort_key == NEW:
            query_set.order_by('-date')
        elif sort_key == LIKE:
            query_set.order_by('-like')

        for post in query_set:
            photo = models.FlexPhotoModel.objects.filter(flex_post__post_id=post.post_id).first()
            if photo:
                post.photo = photo.photo
            post.like = f'{post.like:,}'
            post.price = f'{post.pawn_post.price:,}'

        paginator = Paginator(query_set, 20)
        return paginator.page(page)


class FlexPostRetrieveView(viewsets.generics.RetrieveDestroyAPIView):
    serializer_class = serializers.FlexPostRetrieveSerializer
    model = models.FlexPostModel
    queryset = models.FlexPostModel.objects.all()

    def retrieve(self, request, *args, **kwargs):
        post = self.model.objects.filter(post_id=kwargs['pk']).first()
        if post is None:
            return HttpResponse(status=404)

        post.comments = models.FlexCommentModel.objects.filter(flex_post=post).values()
        post.photos = [photo.photo for photo in models.FlexPhotoModel.objects.filter(flex_post=post)]

        serializer = serializers.FlexPostRetrieveSerializer(post)

        return Response(serializer.data)


class FlexPhotoView(viewsets.generics.CreateAPIView):
    serializer_class = serializers.FlexPhotoSerializer
    model = models.FlexPhotoModel


class FlexCommentView(viewsets.generics.CreateAPIView):
    serializer_class = serializers.FlexCommentSerializer
    model = models.FlexCommentModel


class FlexPostLikeView(viewsets.generics.UpdateAPIView):
    serializer_class = serializers.FlexPostLikeSerializer
    model = models.FlexPostLikeModel

    def update(self, request, *args, **kwargs):
        return Response(status=405)

    def partial_update(self, request, *args, **kwargs):
        user = get_user_model().objects.filter(username=request.data['user']).first()
        like = self.model.objects.filter(user=user).first()
        if like:
            like.flex_post.like -= 1
            like.flex_post.save()

            like.delete()
        else:
            flex_post = models.FlexPostModel.objects.filter(post_id=kwargs['pk']).first()

            flex_post.like += 1
            flex_post.save()
            self.model(flex_post=flex_post, user=user).save()

        return Response(status=201)
