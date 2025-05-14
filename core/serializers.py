from rest_framework import serializers
from .models import MeetingMinutes

class MeetingMinutesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingMinutes
        fields = '__all__'
