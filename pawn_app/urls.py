from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views


app_name = 'pawn'
urlpatterns = [
    path('', views.PawnListView.as_view()),
    path('<int:pk>/', views.PawnPostRetrieveView.as_view()),
    path('image/', views.PawnPhotoView.as_view()),
    path('history/', views.PawnHistoryView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
