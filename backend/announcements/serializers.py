from rest_framework import serializers
from .models import AcademicAnnouncement

class AcademicAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicAnnouncement
        fields = '__all__'
