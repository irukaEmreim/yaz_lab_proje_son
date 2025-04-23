from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import AcademicAnnouncement
from .serializers import AcademicAnnouncementSerializer


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


class AcademicAnnouncementViewSet(viewsets.ModelViewSet):
    queryset = AcademicAnnouncement.objects.all()
    serializer_class = AcademicAnnouncementSerializer

    # Sadece giriş yapmış kullanıcılar erişebilir
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_departments(request):
    from .models import Bolum
    data = [{"id": b.id, "ad": b.ad} for b in Bolum.objects.all()]
    return Response(data)
