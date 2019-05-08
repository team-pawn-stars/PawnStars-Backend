from django.core.paginator import Paginator
from rest_framework import viewsets

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

        paginator = Paginator(query_set, 20)
        return paginator.page(page)


class FlexPhotoView(viewsets.generics.CreateAPIView):
    serializer_class = serializers.FlexPhotoSerializer
    model = models.FlexPhotoModel
