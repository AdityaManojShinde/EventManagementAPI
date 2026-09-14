from django.contrib.auth.models import User
from rest_framework import serializers
from event_app.models import Event, Registration, CheckIn


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "start_at",
            "end_at",
            "image",
            "location",
            "meeting_url",
            "is_online",
        ]


class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = [
            "id",
            "event",
            "email",
            "name",
            "phone",
            "department",
            "course",
            "college",
        ]


class EventCheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckIn
        fields = ["id", "registration", "check_in_at"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]
