from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    ApplicationViewSet, 
    basvuru_yap, belge_yukle, basvurularim, faaliyetler_by_application,
    belgeler_by_application, basvuru_detay, profilim, profil_guncelle,
    sifre_guncelle, juri_basvurulari,aday_bilgileri, faaliyet_turleri_by_application,
    juri_degerlendir
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
    path('juri/basvurularim/', juri_basvurulari),  # 👈 İŞTE BURASI!
    path('aday-bilgileri/<int:app_id>/', aday_bilgileri),
    path('faaliyet-turleri/<int:app_id>/', faaliyet_turleri_by_application),
    path('juri/degerlendir/', juri_degerlendir),


]