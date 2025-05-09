from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    ApplicationViewSet, 
    basvuru_yap, belge_yukle, basvurularim, faaliyetler_by_application,
    belgeler_by_application, basvuru_detay, profilim, profil_guncelle,
    sifre_guncelle, juri_basvurulari,aday_bilgileri, faaliyet_turleri_by_application,
    juri_degerlendir, basvuru_juri_raporlari,  basvuru_sonuclandir, sonuclanacak_basvurular,
    tablo5_olustur, kullanici_listesi
)

router = DefaultRouter()
router.register(r'applications', ApplicationViewSet, basename='applications')

urlpatterns = router.urls + [
    path('basvuru-yap/', basvuru_yap),
    path('belge-yukle/', belge_yukle),
    path('basvurularim/', basvurularim, name='basvurularim'),
    path('faaliyetler/<int:app_id>/', faaliyetler_by_application),
    path('belgeler/<int:app_id>/', belgeler_by_application),
    path('basvuru-detay/<int:app_id>/', basvuru_detay),
    path('profilim/', profilim),
    path('profilim/guncelle/', profil_guncelle),
    path('profilim/sifre/', sifre_guncelle),
    path('juri/basvurularim/', juri_basvurulari),
    path('aday-bilgileri/<int:app_id>/', aday_bilgileri),
    path('faaliyet-turleri/<int:app_id>/', faaliyet_turleri_by_application),
    path('juri/degerlendir/', juri_degerlendir),
    path('basvuru/<int:application_id>/jury-raporlari/', basvuru_juri_raporlari),
    path('basvuru-sonuclandir/<int:application_id>/', basvuru_sonuclandir),
    path('sonuclanacak-basvurular/', sonuclanacak_basvurular),
    path('tablo5/<int:application_id>/', tablo5_olustur),
    path('tablo5-olustur/<int:application_id>/', tablo5_olustur),
    path('kullanicilar/', kullanici_listesi),

]