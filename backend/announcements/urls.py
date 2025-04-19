from rest_framework.routers import DefaultRouter
from .views import AcademicAnnouncementViewSet

router = DefaultRouter()
router.register(r'announcements', AcademicAnnouncementViewSet, basename='announcement')

urlpatterns = router.urls
