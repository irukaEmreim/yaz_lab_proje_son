from django.urls import path
from .views import CustomTokenObtainPairView
from .views import register

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', register),
]
