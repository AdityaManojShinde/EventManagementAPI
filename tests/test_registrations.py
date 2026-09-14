from django.urls import reverse
from rest_framework import status
from event_app.models import Registration
from tests.base import EventTestCase


class RegistrationAPITest(EventTestCase):
    def setUp(self):
        super().setUp()

        self.registration = Registration.objects.create(
            event=self.event,
            email="student@example.com",
            name="John Doe",
            phone="9876543210",
            department="Computer Science",
            course="B.Tech",
            college="MIT ADT University",
        )

    def test_registration_list_requires_admin(self):
        url = reverse("registration-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_registration_list(self):
        self.client.force_authenticate(user=self.admin)

        url = reverse("registration-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_registration_detail(self):
        self.client.force_authenticate(user=self.admin)

        url = reverse(
            "registration-detail",
            args=[self.registration.id],
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_registration_create(self):
        url = reverse("registration-list")

        data = {
            "event": self.event.id,
            "email": "newstudent@example.com",
            "name": "Jane Doe",
            "phone": "9876543211",
            "department": "Computer Science",
            "course": "B.Tech",
            "college": "MIT ADT University",
        }

        response = self.client.post(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_registration_update(self):
        self.client.force_authenticate(user=self.admin)

        url = reverse(
            "registration-detail",
            args=[self.registration.id],
        )

        response = self.client.patch(
            url,
            {"name": "Updated Name"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.registration.refresh_from_db()

        self.assertEqual(
            self.registration.name,
            "Updated Name",
        )

    def test_registration_delete(self):
        self.client.force_authenticate(user=self.admin)

        url = reverse(
            "registration-detail",
            args=[self.registration.id],
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Registration.objects.filter(
                id=self.registration.id,
            ).exists()
        )

    def test_duplicate_registration(self):
        url = reverse("registration-list")

        data = {
            "event": self.event.id,
            "email": self.registration.email,
            "name": "Another Person",
            "phone": "9999999999",
            "department": "IT",
            "course": "B.Tech",
            "college": "MIT ADT University",
        }

        response = self.client.post(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
