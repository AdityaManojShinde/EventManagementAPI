from django.urls import reverse
from rest_framework import status

from event_app.models import CheckIn, Registration
from tests.base import EventTestCase


class CheckInAPITest(EventTestCase):
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

    def test_checkin_requires_admin(self):
        url = reverse("check-in-list")

        response = self.client.post(
            url,
            {"registration": self.registration.id},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_checkin_create(self):
        self.client.force_authenticate(user=self.admin)

        url = reverse("check-in-list")

        response = self.client.post(
            url,
            {"registration": self.registration.id},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            CheckIn.objects.filter(
                registration=self.registration,
            ).exists()
        )

    def test_checkin_list(self):
        self.client.force_authenticate(user=self.admin)

        CheckIn.objects.create(
            registration=self.registration,
        )

        url = reverse("check-in-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_checkin_detail(self):
        self.client.force_authenticate(user=self.admin)

        checkin = CheckIn.objects.create(
            registration=self.registration,
        )

        url = reverse(
            "check-in-detail",
            args=[checkin.id],
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_duplicate_checkin(self):
        self.client.force_authenticate(user=self.admin)

        CheckIn.objects.create(
            registration=self.registration,
        )

        url = reverse("check-in-list")

        response = self.client.post(
            url,
            {"registration": self.registration.id},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_checkin_delete(self):
        self.client.force_authenticate(user=self.admin)

        checkin = CheckIn.objects.create(
            registration=self.registration,
        )

        url = reverse(
            "check-in-detail",
            args=[checkin.id],
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            CheckIn.objects.filter(
                id=checkin.id,
            ).exists()
        )
