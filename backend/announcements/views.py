from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import AcademicAnnouncement
from .serializers import AcademicAnnouncementSerializer

class AcademicAnnouncementViewSet(viewsets.ModelViewSet):
    queryset = AcademicAnnouncement.objects.all()
    serializer_class = AcademicAnnouncementSerializer

    # Sadece giriş yapmış kullanıcılar erişebilir
    permission_classes = [permissions.IsAuthenticated]
