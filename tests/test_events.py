from django.urls import reverse
from rest_framework import status

from event_app.models import Event
from tests.base import EventTestCase


class EventAPITest(EventTestCase):
    def setUp(self):
        super().setUp()

    def test_event_list(self):
        url = reverse("event-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_detail(self):
        url = reverse("event-detail", args=[self.event.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_create_requires_admin(self):
        url = reverse("event-list")

        data = {
            "title": "Django Workshop",
            "description": "Learn Django",
            "start_at": "2026-09-21T10:00:00Z",
            "end_at": "2026-09-21T17:00:00Z",
            "location": "MIT ADT University",
            "meeting_url": "",
            "is_online": False,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_event_create(self):
        self.client.force_authenticate(user=self.admin)

        url = reverse("event-list")

        data = {
            "title": "Django Workshop",
            "description": "Learn Django",
            "start_at": "2026-09-21T10:00:00Z",
            "end_at": "2026-09-21T17:00:00Z",
            "location": "MIT ADT University",
            "meeting_url": "",
            "is_online": False,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_event_update(self):
        self.client.force_authenticate(user=self.admin)

        url = reverse("event-detail", args=[self.event.id])

        response = self.client.patch(
            url,
            {"title": "Updated Python Workshop"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.event.refresh_from_db()

        self.assertEqual(
            self.event.title,
            "Updated Python Workshop",
        )

    def test_event_delete(self):
        self.client.force_authenticate(user=self.admin)

        url = reverse("event-detail", args=[self.event.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Event.objects.filter(id=self.event.id).exists())
