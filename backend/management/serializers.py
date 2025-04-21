from rest_framework import serializers
from .models import Jury, KadroKriterleri, PuanKriterleri, Bolum

class JurySerializer(serializers.ModelSerializer):
    class Meta:
        model = Jury
        fields = '__all__'

class KadroKriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = KadroKriterleri
        fields = '__all__'

class PuanKriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PuanKriterleri
        fields = '__all__'