from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from . import views

urlpatterns = [
    path('signin', obtain_jwt_token),
    path('signup/buyer', views.BuyerUserView.as_view()),
    path('signup/seller', views.SellerUserView.as_view()),
    path('pawn/', views.PawnListView.as_view()),
]
