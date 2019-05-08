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
        if post is None:
            return Response(status=404)

        post.histories = models.PawnHistoryModel.objects.filter(pawn_post=post).values()
        serializer = serializers.PawnPostRetrieveSerializer(post)

        return Response(serializer.data)
