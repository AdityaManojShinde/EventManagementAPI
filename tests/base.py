from django.test import TestCase
from django.contrib.auth.models import User
from event_app.models import Event
from rest_framework.test import APIClient


class EventTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.event = Event.objects.create(
            title="Python Workshop",
            description="Learn Python",
            start_at="2026-09-20T10:00:00Z",
            end_at="2026-09-20T17:00:00Z",
            location="MIT ADT University",
            meeting_url="",
            is_online=False,
        )

        self.admin = User.objects.create_superuser(
            username="admin",
            password="8767",
        )
