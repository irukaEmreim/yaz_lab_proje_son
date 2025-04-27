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


from .models import FaaliyetPuanlari
class FaaliyetPuanSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaaliyetPuanlari
        fields = '__all__'