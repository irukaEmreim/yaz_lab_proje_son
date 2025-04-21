from rest_framework.routers import DefaultRouter
from .views import AssignedApplicationViewSet, get_juries, add_jury, get_available_juries, create_jury, kadro_kriterleri_list_update, puan_kriterleri_list_update
from django.urls import path

router = DefaultRouter()
router.register(r'yonetici/basvurular', AssignedApplicationViewSet, basename='assigned-apps')

urlpatterns = router.urls + [
    path('juri-atamasi/<int:announcement_id>/', get_juries),
    path('juri-ekle/', add_jury),
    path('uygun-juriler/', get_available_juries),
    path('juri-olustur/', create_jury),
    path('kadro-kriterleri/', kadro_kriterleri_list_update),
    path('puan-kriterleri/', puan_kriterleri_list_update),
    
]
