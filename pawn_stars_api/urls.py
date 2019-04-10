from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from . import views

urlpatterns = [
    path('signin/', obtain_jwt_token),
    path('signup/', views.BuyerUserView.as_view())
]
