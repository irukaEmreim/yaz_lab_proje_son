from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from applications.models import Application
from applications.serializers import ApplicationSerializer

from .models import Jury          
from .serializers import JurySerializer         

from users.models import User
from django.utils import timezone

# Yöneticinin kendisine atanmış başvuruları
class AssignedApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(assigned_to=self.request.user.id)

# Bir ilana atanmış jürileri getir
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_juries(request, announcement_id):
    juries = Jury.objects.filter(announcement_id=announcement_id)
    data = []

    for jury in juries:
        user = User.objects.filter(id=jury.jury_member_id).first()
        data.append({
            "id": jury.id,
            "jury_tc": user.tc_kimlik_no if user else "Bilinmiyor"
        })

    return Response(data)

# Yeni jüri ataması yap
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_jury(request):
    tc = request.data.get("tc_kimlik_no")
    announcement_id = request.data.get("announcement_id")

    try:
        user = User.objects.get(tc_kimlik_no=tc, role='juri')
    except User.DoesNotExist:
        return Response({"error": "TC'ye ait jüri bulunamadı."}, status=404)

    # Aynı jüri daha önce atanmış mı kontrolü
    if Jury.objects.filter(announcement_id=announcement_id, jury_member_id=user.id).exists():
        return Response({"error": "Bu jüri zaten atanmış."}, status=400)

    Jury.objects.create(
        announcement_id=announcement_id,
        jury_member_id=user.id,
        assigned_at=timezone.now()  
    )

    return Response({"message": "Jüri ataması başarılı."}, status=201)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_available_juries(request):
    from users.models import User
    juriler = User.objects.filter(role='juri')
    data = [{"id": j.id, "tc_kimlik_no": j.tc_kimlik_no} for j in juriler]
    return Response(data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_jury(request):
    from users.models import User

    data = request.data
    required_fields = ['tc_kimlik_no', 'first_name', 'last_name', 'email', 'password']

    if not all(field in data and data[field] for field in required_fields):
        return Response({'error': 'Tüm alanlar gereklidir.'}, status=400)

    if User.objects.filter(tc_kimlik_no=data['tc_kimlik_no']).exists():
        return Response({'error': 'Bu TC zaten kayıtlı.'}, status=400)

    if User.objects.filter(email=data['email']).exists():
        return Response({'error': 'Bu email zaten kayıtlı.'}, status=400)

    user = User(
        tc_kimlik_no=data['tc_kimlik_no'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        role='juri',
        is_active=True,
        is_staff=False,
        is_superuser=False,
        created_at=timezone.now()
    )
    user.set_password(data['password'])
    user.save()

    return Response({'message': 'Yeni jüri başarıyla oluşturuldu.'}, status=201)
