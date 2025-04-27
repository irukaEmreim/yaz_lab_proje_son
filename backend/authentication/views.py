from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from users.models import User
from django.utils import timezone
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['POST'])
def register(request):
    from django.contrib.auth.hashers import make_password
    data = request.data
    try:
        user = User.objects.create(
            tc_kimlik_no=data['tc_kimlik_no'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=make_password(data['password']),
            role='aday',
            is_active=True,
            crerated_at =timezone.now()
        )
        return Response({"message": "Kayıt başarılı!"})
    except Exception as e:
        print("Kayıt hatası:", e)
        return Response({"error": "Kayıt başarısız"}, status=400)
