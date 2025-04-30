from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Application
from .serializers import ApplicationSerializer
from rest_framework import permissions
from rest_framework.permissions import AllowAny

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from .models import Application, ApplicationActivity, ApplicationDocument
from django.utils import timezone
from announcements.models import AcademicAnnouncement  


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

        # Başvuru olsutrma
        app = Application.objects.create(
            candidate_id=user.id,
            announcement_id=data['announcement_id'],
            status="Beklemede",
            submitted_at=timezone.now()
        )

        for faaliyet_kodu, entry in data.get('form', {}).items():
            ApplicationActivity.objects.create(
                application=app, 
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


from akademik_portal.firebase_config import bucket
from io import BytesIO
from users.models import User
from management.models import FaaliyetPuanlari
from django.utils.text import slugify

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def belge_yukle(request):
    try:
        app_id = request.data.get("application_id")
        file = request.FILES.get("file")
        faaliyet_kodu = request.data.get("faaliyet_kodu")

        if not file:
            return Response({"error": "Dosya eksik"}, status=400)

        app_instance = Application.objects.get(id=app_id)
        aday = User.objects.get(id=app_instance.candidate_id)

        try:
            faaliyet = FaaliyetPuanlari.objects.get(faaliyet_kodu=faaliyet_kodu)
            faaliyet_adi = faaliyet.faaliyet_adi
        except FaaliyetPuanlari.DoesNotExist:
            faaliyet_adi = "Bilinmeyen_Faaliyet"

        aday_klasor_adi = slugify(f"{aday.first_name}_{aday.last_name}").replace('-', '_')
        dosya_adi = slugify(f"{aday.first_name}_{aday.last_name}_{faaliyet_adi}").replace('-', '_') + ".pdf"

        firebase_path = f"basvuru_belgeleri/{aday_klasor_adi}/{dosya_adi}"

        # Firebase'e yükleme
        blob = bucket.blob(firebase_path)
        blob.upload_from_file(file.file, content_type=file.content_type)
        blob.make_public()

        file_url = blob.public_url 

        ApplicationDocument.objects.create(
            application=app_instance,
            file_path=file_url,
            description="",
            uploaded_at=timezone.now(),
            faaliyet_kodu=faaliyet_kodu
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
        if user.role != 'aday':
            return Response({"error": "Yetkisiz erişim."}, status=403)

        basvurular = Application.objects.filter(candidate_id=user.id)

        data = []
        for basvuru in basvurular:
            ilan_baslik = "Başlık bulunamadı"
            try:
                ilan = AcademicAnnouncement.objects.get(id=basvuru.announcement_id)
                ilan_baslik = ilan.title
            except AcademicAnnouncement.DoesNotExist:
                pass  

            data.append({
                "id": basvuru.id,
                "announcement_id": basvuru.announcement_id,
                "announcement_title": ilan_baslik,
                "status": basvuru.status,
                "submitted_at": basvuru.submitted_at,
                "file_path" : basvuru.tablo5_pdf_path,  
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
            "faaliyet_kodu": b.faaliyet_kodu  

        } for b in belgeler]
        return Response(data)
    except Exception as e:
        print("Belge listesi hatası:", e)
        return Response({"error": "Belgeler alınamadı"}, status=500)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def basvuru_detay(request, app_id):
    try:
        from applications.models import Application
        app = Application.objects.get(id=app_id)
        
        basvuru = Application.objects.get(id=app_id)
        data = {
            "id": basvuru.id,
            "announcement_id": basvuru.announcement_id,
            "status": basvuru.status,
            "submitted_at": basvuru.submitted_at,
            "tablo5_pdf_path": app.tablo5_pdf_path,  
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

    from .models import Jury, JuryReport
    from applications.models import Application
    from announcements.models import AcademicAnnouncement, Bolum

    assigned_announcements = Jury.objects.filter(jury_member_id=user.id).values_list('announcement_id', flat=True)

    degerlendirilen_app_ids = JuryReport.objects.filter(
        jury_member_id=user.id
    ).values_list('application_id', flat=True)

    basvurular = Application.objects.filter(
        announcement_id__in=assigned_announcements
    ).exclude(id__in=degerlendirilen_app_ids)

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
            "id": basvuru.id,  
            "announcement_title": ilan_baslik, 
            "end_date": son_basvuru_tarihi,  
            "department_name": bolum_adi,  
            "status": basvuru.status, 
            "submitted_at": basvuru.submitted_at, 
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
                "tc_kimlik_no": aday.tc_kimlik_no, 
                "tablo5_pdf_path": application.tablo5_pdf_path  
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
        from management.models import FaaliyetPuanlari  
        
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
        user = request.user  
        if user.role != 'juri':
            return Response({"error": "Yetkisiz erişim"}, status=403)

        application_id = request.data.get('application_id')
        evaluation_result = request.data.get('sonuc')
        description = request.data.get('degerlendirme_notu')
        dosya = request.FILES.get('dosya')

        if not application_id or not evaluation_result or not dosya or not description:
            return Response({"error": "Eksik veri gönderildi."}, status=400)

        from applications.models import Application
        from users.models import User
        from .models import JuryReport
        from django.utils.text import slugify

        app_instance = Application.objects.get(id=application_id)
        aday = User.objects.get(id=app_instance.candidate_id)

        juri = user  

        dosya_adi = slugify(f"{juri.first_name}_{juri.last_name}_degerlendirme_{aday.first_name}_{aday.last_name}") + ".pdf"

        aday_klasor_adi = slugify(f"{aday.first_name}_{aday.last_name}").replace('-', '_')
        firebase_path = f"juri_raporlari/{aday_klasor_adi}/{dosya_adi}"

        blob = bucket.blob(firebase_path)
        blob.upload_from_file(dosya.file, content_type=dosya.content_type)
        blob.make_public()

        file_url = blob.public_url

        JuryReport.objects.create(
            application_id=application_id,
            jury_member_id=user.id,
            evaluation_result=evaluation_result,
            report_file_path=file_url,
            description=description,
            submitted_at=timezone.now(),
        )

        return Response({"message": "Değerlendirme başarıyla kaydedildi."})

    except Exception as e:
        print("Jüri değerlendirme hatası:", e)
        return Response({"error": "Bir hata oluştu."}, status=500)



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def sonuclanacak_basvurular(request):
    user = request.user

    if user.role != 'yonetici':
        return Response({"error": "Yetkisiz erişim"}, status=403)

    from applications.models import Application
    from management.models import Jury
    from .models import JuryReport
    from announcements.models import AcademicAnnouncement, Bolum

    applications = Application.objects.filter(status='Beklemede')  

    sonuclanacaklar = []

    for app in applications:
        degerlendirme_var_mi = JuryReport.objects.filter(application_id=app.id).exists()

        if not degerlendirme_var_mi:
            continue  

        try:
            ilan = AcademicAnnouncement.objects.get(id=app.announcement_id)
            ilan_baslik = ilan.title
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
            bolum_adi = "Bölüm bilgisi yok"

        sonuclanacaklar.append({
            "application_id": app.id,
            "announcement_title": ilan_baslik,
            "department_name": bolum_adi,
            "status": app.status,
            "submitted_at": app.submitted_at
        })

    return Response(sonuclanacaklar)




@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def basvuru_juri_raporlari(request, application_id):
    user = request.user

    if user.role != 'yonetici':
        return Response({"error": "Yetkisiz erişim"}, status=403)

    from .models import JuryReport
    from users.models import User

    try:
        raporlar = JuryReport.objects.filter(application_id=application_id)

        data = []
        for rapor in raporlar:
            try:
                juri = User.objects.get(id=rapor.jury_member_id)
                juri_adi = f"{juri.first_name} {juri.last_name}"
            except User.DoesNotExist:
                juri_adi = "Bilinmeyen Jüri"

            data.append({
                "jury_member_name": juri_adi,
                "evaluation_result": rapor.evaluation_result,  
                "report_file_path": rapor.report_file_path,    
                "description": rapor.description,              
                "submitted_at": rapor.submitted_at,            
            })

        return Response(data)

    except Exception as e:
        print("Jüri raporları çekilemedi:", e)
        return Response({"error": "Jüri raporları bulunamadı."}, status=500)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def basvuru_sonuclandir(request, application_id):
    user = request.user

    if user.role != 'yonetici':
        return Response({"error": "Yetkisiz erişim"}, status=403)

    from applications.models import Application

    try:
        app = Application.objects.get(id=application_id)
        yeni_status = request.data.get('status')

        if yeni_status not in ['Onaylandı', 'Reddedildi']:
            return Response({"error": "Geçersiz durum."}, status=400)

        app.status = yeni_status
        app.save()

        return Response({"message": "Başvuru durumu başarıyla güncellendi."})

    except Application.DoesNotExist:
        return Response({"error": "Başvuru bulunamadı."}, status=404)

    except Exception as e:
        print("Başvuru sonuçlandırma hatası:", e)
        return Response({"error": "Bir hata oluştu."}, status=500)


from weasyprint import HTML
from django.http import HttpResponse
from django.template.loader import render_to_string
import os

from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse
import datetime

from management.models import FaaliyetPuanlari
from applications.models import ApplicationDocument
from users.models import User
from management.models import Bolum
from django.utils.timezone import now  
import os
from django.conf import settings

@api_view(['GET'])
@permission_classes([AllowAny])
def tablo5_olustur(request, application_id):
    try:
        app = Application.objects.get(id=application_id)
        aday = User.objects.get(id=app.candidate_id)
        ilan = AcademicAnnouncement.objects.get(id=app.announcement_id)

        bolum = None
        if ilan.bolum_id:
            try:
                bolum = Bolum.objects.get(id=ilan.bolum_id)
            except Bolum.DoesNotExist:
                pass

        tarih = timezone.now().strftime('%d.%m.%Y')

        belgeler = ApplicationDocument.objects.filter(application=app)

        faaliyetler_A = FaaliyetPuanlari.objects.filter(faaliyet_kodu__startswith='A')
        faaliyet_puanlama_A = []
        toplam_puan_A = 0
        for faaliyet in faaliyetler_A:
            belge_sayisi = belgeler.filter(faaliyet_kodu=faaliyet.faaliyet_kodu).count()
            toplam = belge_sayisi * faaliyet.puan
            toplam_puan_A += toplam
            faaliyet_puanlama_A.append({'aciklama': faaliyet.aciklama, 'puan': toplam})

        faaliyetler_B = FaaliyetPuanlari.objects.filter(faaliyet_kodu__startswith='B')
        faaliyet_puanlama_B = []
        toplam_puan_B = 0
        for faaliyet in faaliyetler_B:
            belge_sayisi = belgeler.filter(faaliyet_kodu=faaliyet.faaliyet_kodu).count()
            toplam = belge_sayisi * faaliyet.puan
            toplam_puan_B += toplam
            faaliyet_puanlama_B.append({'aciklama': faaliyet.aciklama, 'puan': toplam})

        faaliyetler_C = FaaliyetPuanlari.objects.filter(faaliyet_kodu__startswith='C')
        faaliyet_puanlama_C = []
        toplam_puan_C = 0
        for faaliyet in faaliyetler_C:
            belge_sayisi = belgeler.filter(faaliyet_kodu=faaliyet.faaliyet_kodu).count()
            toplam = belge_sayisi * faaliyet.puan
            toplam_puan_C += toplam
            faaliyet_puanlama_C.append({'aciklama': faaliyet.aciklama, 'puan': toplam})

        faaliyetler_D = FaaliyetPuanlari.objects.filter(faaliyet_kodu__startswith='D')
        faaliyet_puanlama_D = []
        toplam_puan_D = 0
        for faaliyet in faaliyetler_D:
            belge_sayisi = belgeler.filter(faaliyet_kodu=faaliyet.faaliyet_kodu).count()
            toplam = belge_sayisi * faaliyet.puan
            toplam_puan_D += toplam
            faaliyet_puanlama_D.append({'aciklama': faaliyet.aciklama, 'puan': toplam})

        faaliyetler_E = FaaliyetPuanlari.objects.filter(faaliyet_kodu__startswith='E')
        faaliyet_puanlama_E = []
        toplam_puan_E = 0
        for faaliyet in faaliyetler_E:
            belge_sayisi = belgeler.filter(faaliyet_kodu=faaliyet.faaliyet_kodu).count()
            toplam = belge_sayisi * faaliyet.puan
            toplam_puan_E += toplam
            faaliyet_puanlama_E.append({'aciklama': faaliyet.aciklama, 'puan': toplam})

        faaliyetler_F = FaaliyetPuanlari.objects.filter(faaliyet_kodu__startswith='F')
        faaliyet_puanlama_F = []
        toplam_puan_F = 0
        for faaliyet in faaliyetler_F:
            belge_sayisi = belgeler.filter(faaliyet_kodu=faaliyet.faaliyet_kodu).count()
            toplam = belge_sayisi * faaliyet.puan
            toplam_puan_F += toplam
            faaliyet_puanlama_F.append({'aciklama': faaliyet.aciklama, 'puan': toplam})
        
        faaliyetler_G = FaaliyetPuanlari.objects.filter(faaliyet_kodu__startswith='G')
        faaliyet_puanlama_G = []
        toplam_puan_G = 0
        for faaliyet in faaliyetler_G:
            belge_sayisi = belgeler.filter(faaliyet_kodu=faaliyet.faaliyet_kodu).count()
            toplam = belge_sayisi * faaliyet.puan
            toplam_puan_G += toplam
            faaliyet_puanlama_G.append({'aciklama': faaliyet.aciklama, 'puan': toplam})
        
        faaliyetler_H = FaaliyetPuanlari.objects.filter(faaliyet_kodu__startswith='H')
        faaliyet_puanlama_H = []
        toplam_puan_H = 0
        for faaliyet in faaliyetler_H:
            belge_sayisi = belgeler.filter(faaliyet_kodu=faaliyet.faaliyet_kodu).count()
            toplam = belge_sayisi * faaliyet.puan
            toplam_puan_H += toplam
            faaliyet_puanlama_H.append({'aciklama': faaliyet.aciklama, 'puan': toplam})

        faaliyetler_I = FaaliyetPuanlari.objects.filter(faaliyet_kodu__startswith='I')
        faaliyet_puanlama_I = []
        toplam_puan_I = 0
        for faaliyet in faaliyetler_I:
            belge_sayisi = belgeler.filter(faaliyet_kodu=faaliyet.faaliyet_kodu).count()
            toplam = belge_sayisi * faaliyet.puan
            toplam_puan_I += toplam
            faaliyet_puanlama_I.append({'aciklama': faaliyet.aciklama, 'puan': toplam})

        faaliyetler_J = FaaliyetPuanlari.objects.filter(faaliyet_kodu__startswith='J')
        faaliyet_puanlama_J = []
        toplam_puan_J = 0
        for faaliyet in faaliyetler_J:
            belge_sayisi = belgeler.filter(faaliyet_kodu=faaliyet.faaliyet_kodu).count()
            toplam = belge_sayisi * faaliyet.puan
            toplam_puan_J += toplam
            faaliyet_puanlama_J.append({'aciklama': faaliyet.aciklama, 'puan': toplam})

        faaliyetler_K = FaaliyetPuanlari.objects.filter(faaliyet_kodu__startswith='K')
        faaliyet_puanlama_K = []
        toplam_puan_K = 0
        for faaliyet in faaliyetler_K:
            belge_sayisi = belgeler.filter(faaliyet_kodu=faaliyet.faaliyet_kodu).count()
            toplam = belge_sayisi * faaliyet.puan
            toplam_puan_K += toplam
            faaliyet_puanlama_K.append({'aciklama': faaliyet.aciklama, 'puan': toplam})


        genel_toplam_puan = (
            toplam_puan_A + toplam_puan_B + toplam_puan_C +
            toplam_puan_D + toplam_puan_E + toplam_puan_F +
            toplam_puan_G + toplam_puan_H + toplam_puan_I +
            toplam_puan_J + toplam_puan_K
        )

        html_string = render_to_string('tablo5_template.html', {
            'ad_soyad': f"{aday.first_name} {aday.last_name}",
            'kadro': ilan.position_type,
            'bolum': bolum.ad if bolum else "Bölüm Bilgisi Yok",
            'tarih': tarih,
            'faaliyet_puanlama_A': faaliyet_puanlama_A,
            'toplam_puan_A': toplam_puan_A,
            'faaliyet_puanlama_B': faaliyet_puanlama_B,
            'toplam_puan_B': toplam_puan_B,
            'faaliyet_puanlama_C': faaliyet_puanlama_C,
            'toplam_puan_C': toplam_puan_C,
            'faaliyet_puanlama_D': faaliyet_puanlama_D,
            'toplam_puan_D': toplam_puan_D,
            'faaliyet_puanlama_E': faaliyet_puanlama_E,
            'toplam_puan_E': toplam_puan_E,
            'faaliyet_puanlama_F': faaliyet_puanlama_F,  
            'toplam_puan_F': toplam_puan_F,
            'faaliyet_puanlama_G' : faaliyet_puanlama_G,
            'toplam_puan_G' : toplam_puan_G,
            'faaliyet_puanlama_H': faaliyet_puanlama_H,  
            'toplam_puan_H': toplam_puan_H,
            'faaliyet_puanlama_I': faaliyet_puanlama_I,  
            'toplam_puan_I': toplam_puan_I,
            'faaliyet_puanlama_J': faaliyet_puanlama_J,  
            'toplam_puan_J': toplam_puan_J,              
            'faaliyet_puanlama_K': faaliyet_puanlama_K, 
            'toplam_puan_K': toplam_puan_K,             
            'genel_toplam_puan': genel_toplam_puan,  
        })

        html = HTML(string=html_string)
        pdf = html.write_pdf()
        from akademik_portal.firebase_config import bucket
        from io import BytesIO
        
        pdf_buffer = BytesIO()
        pdf_buffer.write(pdf)
        pdf_buffer.seek(0)  


        blob = bucket.blob(f"tablo5/tablo5_{application_id}.pdf")
        blob.upload_from_file(pdf_buffer, content_type="application/pdf")
        blob.make_public()

        app.tablo5_pdf_path = blob.public_url
        app.save()


        return Response ({"message": "Tablo 5 başarıyla oluşturuldu ve Firebase'e kaydedildi."}) 
        

    except Exception as e:
        print("Tablo 5 oluşturulamadı:", e)
        return Response({"error": "Tablo 5 oluşturulamadı."}, status=500)
"""

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def tablo5_olustur(request, application_id):
    from weasyprint import HTML
    from django.template.loader import render_to_string
    import os
    from django.conf import settings

    try:
        app = Application.objects.get(id=application_id)
        aday = User.objects.get(id=app.candidate_id)
        ilan = AcademicAnnouncement.objects.get(id=app.announcement_id)

        bolum = None
        if ilan.bolum_id:
            try:
                bolum = Bolum.objects.get(id=ilan.bolum_id)
            except Bolum.DoesNotExist:
                pass

        tarih = timezone.now().strftime('%d.%m.%Y')

        faaliyetler = FaaliyetPuanlari.objects.all()
        belgeler = ApplicationDocument.objects.filter(application=app)

        faaliyet_puanlama_listesi = []
        for faaliyet in faaliyetler:
            belge_sayisi = belgeler.filter(faaliyet_kodu=faaliyet.faaliyet_kodu).count()
            toplam_puan = belge_sayisi * faaliyet.puan

            faaliyet_puanlama_listesi.append({
                'kategori': faaliyet.faaliyet_kodu[0],
                'aciklama': faaliyet.aciklama,
                'puan': toplam_puan
            })

        html_string = render_to_string('tablo5_template.html', {
            'ad_soyad': f"{aday.first_name} {aday.last_name}",
            'kadro': ilan.position_type,
            'bolum': bolum.ad if bolum else "Bölüm Bilgisi Yok",
            'tarih': tarih,
            'faaliyet_puanlama_listesi': faaliyet_puanlama_listesi
        })

        html = HTML(string=html_string)
        pdf_file = html.write_pdf()

        pdf_folder = os.path.join(settings.MEDIA_ROOT, 'tablo5')
        os.makedirs(pdf_folder, exist_ok=True)

        pdf_filename = f"tablo5_{app.id}.pdf"
        pdf_path = os.path.join(pdf_folder, pdf_filename)

        with open(pdf_path, 'wb') as f:
            f.write(pdf_file)

        app.tablo5_pdf_path = f'tablo5/{pdf_filename}'
        app.save()

        return Response({"message": "Tablo5 başarıyla oluşturuldu ve kaydedildi."})

    except Exception as e:
        print("Tablo 5 oluşturulamadı:", e)
        return Response({"error": "Tablo 5 oluşturulamadı."}, status=500)
"""

from users.models import User

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def kullanici_listesi(request):
    if not request.user.is_superuser and request.user.role != 'admin':
        return Response({"error": "Yetkisiz erişim"}, status=403)
    
    users = User.objects.all()
    print("Tüm kullanıcılar:", users)  
    
    data = []
    for user in users:
        data.append({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": user.created_at,
        })
    return Response(data)