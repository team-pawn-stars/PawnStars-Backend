from django.core.paginator import Paginator

from rest_framework import viewsets
from rest_framework.response import Response

from const import CATEGORY, SORT_KEY, REGION, PAGE, QUERY, ALL, NEW
from exception import BadRequestException
from . import serializers, models


class PawnListView(viewsets.generics.ListCreateAPIView):
    serializer_class = serializers.PawnPostListSerializer
    model: models.PawnPostModel = models.PawnPostModel

    def get_queryset(self):
        query_params = self.request.query_params

        category = query_params.get(CATEGORY, ALL)
        sort_key = query_params.get(SORT_KEY, NEW)
        region = query_params.get(REGION)
        page = query_params.get(PAGE, 1)
        query = query_params.get(QUERY)

        if region is None:
            raise BadRequestException()

        query_set: models.models.QuerySet = self.model.objects.filter(region=region)

        if category != ALL:
            query_set = query_set.filter(category=category)

        if query is not None:
            query_set = query_set.filter(title__contains=query)

        if sort_key == NEW:
            query_set = query_set.order_by('-date')
        else:
            query_set = query_set.order_by('-like')
        for post in query_set:
            photo = models.PawnPhotoModel.objects.filter(pawn_post__post_id=post.post_id).first()

            if photo:
                post.photo = photo.photo
            post.price = f'{post.price:,}'
            post.like = f'{post.like:,}'

        paginator = Paginator(query_set, 20)
        return paginator.page(page)


class PawnLikeListView(viewsets.generics.ListCreateAPIView):
    serializer_class = serializers.PawnPostListSerializer
    model: models.PawnPostModel = models.PawnPostModel

    def get_queryset(self):
        post_ids = [like.pawn_post.post_id for like in models.PawnPostLikeModel.objects.filter(user=self.request.user)]

        query_set: models.models.QuerySet = self.model.objects.filter(post_id__in=post_ids).all()
        query_set = query_set.order_by('-date')

        query_params = self.request.query_params
        page = query_params.get(PAGE, 1)
        for post in query_set:
            photo = models.PawnPhotoModel.objects.filter(pawn_post=post).first()

            if photo:
                post.photo = photo.photo
            post.price = f'{post.price:,}'
            post.like = f'{post.like:,}'

        paginator = Paginator(query_set, 20)
        return paginator.page(page)


class PawnPhotoView(viewsets.generics.CreateAPIView):
    serializer_class = serializers.PawnPhotoSerializer
    model: models.PawnPhotoModel = models.PawnPhotoModel


class PawnHistoryView(viewsets.generics.CreateAPIView):
    serializer_class = serializers.PawnHistorySerializer
    model = models.PawnHistoryModel


class PawnPostRetrieveView(viewsets.generics.RetrieveDestroyAPIView):
    serializer_class = serializers.PawnPostRetrieveSerializer
    model = models.PawnPostModel
    queryset = models.PawnPostModel.objects.all()

    def retrieve(self, request, *args, **kwargs):
        post = self.model.objects.filter(post_id=kwargs['pk']).first()
        like = models.PawnPostLikeModel.objects.filter(user=request.user, pawn_post=post).first()

        if post is None:
            return Response(status=404)

        post.liked = bool(like)
        post.like = f'{post.like:,}'
        post.price = f'{post.price:,}'
        post.histories = models.PawnHistoryModel.objects.filter(pawn_post=post).values()
        post.photos = [photo.photo for photo in models.PawnPhotoModel.objects.filter(pawn_post=post)]
        serializer = serializers.PawnPostRetrieveSerializer(post)

        return Response(serializer.data)


class PawnPostLikeView(viewsets.generics.UpdateAPIView):
    serializer_class = serializers.PawnPostLikeSerializer
    model = models.PawnPostLikeModel

    def update(self, request, *args, **kwargs):
        return Response(status=405)

    def partial_update(self, request, *args, **kwargs):
        like = self.model.objects.filter(user=request.user).first()
        pawn_post = models.PawnPostModel.objects.filter(post_id=kwargs['pk']).first()

        if pawn_post is None:
            return Response(status=404)
        if like:
            pawn_post.like -= 1
            pawn_post.save()

            like.delete()
        else:
            pawn_post.like += 1
            pawn_post.save()
            self.model(pawn_post=pawn_post, user=request.user).save()

        return Response(status=201)
