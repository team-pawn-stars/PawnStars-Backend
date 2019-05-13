from django.urls import path

from . import views

app_name = 'flex'
urlpatterns = [
    path('', views.FlexPostListView.as_view(), name='flex_list'),
    path('<int:pk>/', views.FlexPostRetrieveView.as_view(), name='flex_retrieve'),
    path('<int:pk>/like/', views.FlexPostLikeView.as_view(), name='flex_like'),
    path('image/', views.FlexPhotoView.as_view(), name='flex_image'),
    path('comment/', views.FlexCommentView.as_view(), name='flex_comment')
]
