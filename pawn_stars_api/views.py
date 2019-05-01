from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from rest_framework import viewsets

from const import CATEGORY, SORT_KEY, REGION, PAGE, QUERY, ALL, NEW
from exception import BadRequestException
from . import serializers, models


class BuyerUserView(viewsets.generics.CreateAPIView):
    serializer_class = serializers.BuyerUserSerializer
    model = get_user_model()


class SellerUserView(viewsets.generics.CreateAPIView):
    serializer_class = serializers.SellerUserSerializer
    model = get_user_model()


class PawnListView(viewsets.generics.ListAPIView):
    serializer_class = serializers.PawnPostSerializer
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
            post.photo = models.PawnPhotoModel.objects.filter(pawn_post__post_id=post.post_id).first().photo
            post.price = f'{post.price:,}'
            post.like = f'{post.like:,}'

        paginator = Paginator(query_set, 20)

        return paginator.page(page)


class PawnPhotoView(viewsets.generics.CreateAPIView):
    serializer_class = serializers.PawnPhotoSerializer
    model: models.PawnPhotoModel = models.PawnPhotoModel
