from django.urls import path

from . import views


app_name = 'flex'
urlpatterns = [
    path('', views.FlexPostListView.as_view(), name='flex_list'),
]
