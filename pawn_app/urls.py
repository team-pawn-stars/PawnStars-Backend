from django.urls import path

from . import views

app_name = 'pawn'
urlpatterns = [
    path('', views.PawnListView.as_view()),
    path('<int:pk>/', views.PawnPostRetrieveView.as_view()),
    path('<int:pk>/like/', views.PawnPostLikeView.as_view()),
    path('image/', views.PawnPhotoView.as_view()),
    path('history/', views.PawnHistoryView.as_view()),
]

