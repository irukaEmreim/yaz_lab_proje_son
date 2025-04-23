from rest_framework.routers import DefaultRouter
from .views import AcademicAnnouncementViewSet
from django.urls import path
from .views import get_departments

router = DefaultRouter()
router.register(r'announcements', AcademicAnnouncementViewSet, basename='announcement')

urlpatterns = router.urls + [
    path('bolumler/', get_departments),
]
