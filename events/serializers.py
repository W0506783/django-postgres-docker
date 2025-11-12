from rest_framework import serializers
from .models import Attendee, Event, Registration

class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = "__all__"

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = "__all__"