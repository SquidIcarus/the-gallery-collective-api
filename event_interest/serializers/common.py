from rest_framework import serializers
from ..models import EventInterest

class EventInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventInterest
        fields = '__all__'