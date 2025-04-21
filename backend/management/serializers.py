from rest_framework import serializers
from .models import Jury

class JurySerializer(serializers.ModelSerializer):
    class Meta:
        model = Jury
        fields = '__all__'
