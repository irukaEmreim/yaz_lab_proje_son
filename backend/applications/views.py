from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Application
from .serializers import ApplicationSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from .models import Application, ApplicationActivity, ApplicationDocument
from django.utils import timezone
from announcements.models import AcademicAnnouncement  # İlan modelini import et


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]  

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def basvuru_yap(request):
    user = request.user
    data = request.data

    try:
        print("Gelen veri:", data)

        # Başvuru oluştur
        app = Application.objects.create(
            candidate_id=user.id,
            announcement_id=data['announcement_id'],
            status="Beklemede",
            submitted_at=timezone.now()
        )

        # Faaliyetleri kaydet
        for faaliyet_kodu, entry in data.get('form', {}).items():
            ApplicationActivity.objects.create(
                application=app,  # ✅ dikkat! burada application_id yazıyoruz
                faaliyet_kodu=faaliyet_kodu,
                adet=entry['adet'],
                created_at=timezone.now()
            )

        return Response({
            "message": "Başvuru başarıyla kaydedildi",
            "application_id": app.id
        }, status=201)

    except Exception as e:
        print("Başvuru sırasında hata:", e)
        return Response({"error": "Başvuru sırasında bir hata oluştu."}, status=500)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def belge_yukle(request):
    try:
        app_id = request.data.get("application_id")
        file = request.FILES.get("file")
        faaliyet_kodu = request.data.get("faaliyet_kodu")  # 🔥 burada yakalıyoruz

        if not file:
            return Response({"error": "Dosya eksik"}, status=400)

        app_instance = Application.objects.get(id=app_id)

        ApplicationDocument.objects.create(
            application=app_instance,  # instance veriyoruz
            file_path=file.name,        # dosya ismi
            description="",             # istersen açıklama buraya yazarsın
            uploaded_at=timezone.now(),
            faaliyet_kodu=faaliyet_kodu  # 🔥 burada kaydediyoruz

        )

        return Response({"message": "Belge kaydedildi"}, status=201)

    except Exception as e:
        print("Belge yükleme hatası:", e)
        return Response({"error": "Belge yüklenemedi"}, status=500)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def basvurularim(request):
    user = request.user
    try:
        basvurular = Application.objects.filter(candidate_id=user.id)

        data = []
        for basvuru in basvurular:
            try:
                ilan = AcademicAnnouncement.objects.get(id=basvuru.announcement_id)
                ilan_baslik = ilan.title
            except AcademicAnnouncement.DoesNotExist:
                ilan_baslik = "Başlık bulunamadı"

            data.append({
                "id": basvuru.id,
                "announcement_id": basvuru.announcement_id,
                "announcement_title": ilan_baslik,   # 📢 yeni eklenen kısım
                "status": basvuru.status,
                "submitted_at": basvuru.submitted_at,
            })

        return Response(data, status=200)

    except Exception as e:
        print("Başvurularımı listelerken hata:", e)
        return Response({"error": "Başvurular alınamadı."}, status=500)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def faaliyetler_by_application(request, app_id):
    try:
        faaliyetler = ApplicationActivity.objects.filter(application_id=app_id)
        data = [{
            "id": f.id,
            "faaliyet_kodu": f.faaliyet_kodu,
            "adet": f.adet,
            "created_at": f.created_at
        } for f in faaliyetler]
        return Response(data)
    except Exception as e:
        print("Faaliyet listesi hatası:", e)
        return Response({"error": "Faaliyetler alınamadı"}, status=500)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def belgeler_by_application(request, app_id):
    try:
        belgeler = ApplicationDocument.objects.filter(application_id=app_id)
        data = [{
            "id": b.id,
            "file_path": b.file_path,
            "description": b.description,
            "uploaded_at": b.uploaded_at,
            "faaliyet_kodu": b.faaliyet_kodu  # 🔥 FAALİYET KODUNU DA EKLİYORUZ

        } for b in belgeler]
        return Response(data)
    except Exception as e:
        print("Belge listesi hatası:", e)
        return Response({"error": "Belgeler alınamadı"}, status=500)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def basvuru_detay(request, app_id):
    try:
        basvuru = Application.objects.get(id=app_id)
        data = {
            "id": basvuru.id,
            "announcement_id": basvuru.announcement_id,
            "status": basvuru.status,
            "submitted_at": basvuru.submitted_at,
        }
        return Response(data)
    except Application.DoesNotExist:
        return Response({"error": "Başvuru bulunamadı."}, status=404)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profilim(request):
    user = request.user
    return Response({
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    })

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def profil_guncelle(request):
    user = request.user
    data = request.data
    try:
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.email = data.get("email", user.email)
        user.save()
        return Response({"message": "Profil güncellendi"})
    except Exception as e:
        print("Profil güncelleme hatası:", e)
        return Response({"error": "Güncelleme başarısız"}, status=500)

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def sifre_guncelle(request):
    user = request.user
    data = request.data

    old_password = data.get("old_password")
    new_password = data.get("new_password")

    if not user.check_password(old_password):
        return Response({"error": "Mevcut şifre yanlış"}, status=400)

    user.set_password(new_password)
    user.save()
    return Response({"message": "Şifre başarıyla güncellendi"})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def juri_basvurulari(request):
    user = request.user

    if user.role != 'juri':
        return Response({"error": "Yetkisiz erişim"}, status=403)

    from management.models import Jury
    from applications.models import Application
    from announcements.models import AcademicAnnouncement, Bolum

    assigned_announcements = Jury.objects.filter(jury_member_id=user.id).values_list('announcement_id', flat=True)

    basvurular = Application.objects.filter(announcement_id__in=assigned_announcements)

    data = []
    for basvuru in basvurular:
        try:
            ilan = AcademicAnnouncement.objects.get(id=basvuru.announcement_id)
            ilan_baslik = ilan.title
            son_basvuru_tarihi = ilan.end_date
            bolum_adi = None
            if ilan.bolum_id:
                try:
                    bolum = Bolum.objects.get(id=ilan.bolum_id)
                    bolum_adi = bolum.ad
                except Bolum.DoesNotExist:
                    bolum_adi = "Bölüm bulunamadı"
            else:
                bolum_adi = "Bölüm bilgisi yok"
        except AcademicAnnouncement.DoesNotExist:
            ilan_baslik = "Başlık bulunamadı"
            son_basvuru_tarihi = None
            bolum_adi = "Bölüm bilgisi yok"

        data.append({
            "id": basvuru.id,  # Başvuru Numarası
            "announcement_title": ilan_baslik,  # İlan Başlığı
            "end_date": son_basvuru_tarihi,  # Son Başvuru Tarihi
            "department_name": bolum_adi,  # Bölüm Adı
            "status": basvuru.status,  # Başvuru Durumu
            "submitted_at": basvuru.submitted_at,  # Başvuru Tarihi
        })

    return Response(data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def aday_bilgileri(request, app_id):
    try:
        from applications.models import Application
        from users.models import User

        application = Application.objects.get(id=app_id)
        aday = User.objects.get(id=application.candidate_id)

        data = {
            "first_name": aday.first_name,
            "last_name": aday.last_name,
            "email": aday.email,
            "tc_kimlik_no": aday.tc_kimlik_no,  # Eğer göstermek istersen
        }
        return Response(data)

    except Exception as e:
        print("Aday bilgisi çekilemedi:", e)
        return Response({"error": "Aday bilgisi bulunamadı."}, status=500)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def faaliyet_turleri_by_application(request, app_id):
    try:
        from applications.models import ApplicationActivity
        from management.models import FaaliyetPuanlari  # veya faaliyet_puanlari tablosunu temsil eden model
        
        faaliyetler = ApplicationActivity.objects.filter(application_id=app_id)

        faaliyet_listesi = []

        for faaliyet in faaliyetler:
            try:
                faaliyet_adi = FaaliyetPuanlari.objects.get(faaliyet_kodu=faaliyet.faaliyet_kodu).faaliyet_adi
            except FaaliyetPuanlari.DoesNotExist:
                faaliyet_adi = "Bilinmeyen Faaliyet"

            faaliyet_listesi.append({
                "faaliyet_kodu": faaliyet.faaliyet_kodu,
                "faaliyet_adi": faaliyet_adi
            })

        return Response(faaliyet_listesi)

    except Exception as e:
        print("Faaliyet türleri çekilemedi:", e)
        return Response({"error": "Faaliyet türleri bulunamadı."}, status=500)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def juri_degerlendir(request):
    try:
        user = request.user  # juri kullanıcı
        if user.role != 'juri':
            return Response({"error": "Yetkisiz erişim"}, status=403)

        application_id = request.data.get('application_id')
        evaluation_result = request.data.get('sonuc')  # 'olumlu' veya 'olumsuz'
        description = request.data.get('degerlendirme_notu')  # 🔥 Açıklama geliyor!
        dosya = request.FILES.get('dosya')

        if not application_id or not evaluation_result or not dosya or not description:
            return Response({"error": "Eksik veri gönderildi."}, status=400)

        # Dosyayı kaydet (örnek: /uploads/jury_reports klasörüne)
        import os
        from django.conf import settings

        save_path = os.path.join(settings.MEDIA_ROOT, 'jury_reports', dosya.name)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'wb+') as destination:
            for chunk in dosya.chunks():
                destination.write(chunk)

        from .models import JuryReport
        JuryReport.objects.create(
            application_id=application_id,
            jury_member_id=user.id,
            evaluation_result=evaluation_result,
            report_file_path=f'jury_reports/{dosya.name}',  # Göreli dosya yolu
            description=description,  # 🔥 Açıklamayı da kaydediyoruz
            submitted_at=timezone.now(),
        )

        return Response({"message": "Değerlendirme başarıyla kaydedildi."})

    except Exception as e:
        print("Jüri değerlendirme hatası:", e)
        return Response({"error": "Bir hata oluştu."}, status=500)
