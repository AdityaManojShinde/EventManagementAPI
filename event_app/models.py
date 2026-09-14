import uuid
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Event(models.Model):
    class Meta:
        ordering = ["-start_at"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = CKEditor5Field("Description", config_name="extends")
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    image = models.ImageField(upload_to="events/%Y/%m/%d", null=True, blank=True)
    location = models.CharField(max_length=500, blank=True)
    meeting_url = models.URLField(blank=True)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Registration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="registrations"
    )
    email = models.EmailField()
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    department = models.CharField(max_length=200)
    course = models.CharField(max_length=200)
    college = models.CharField(max_length=200)

    class Meta:
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(
                fields=["event", "email"],
                name="unique_event_registration",
            )
        ]

    def __str__(self):
        return self.email


class CheckIn(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    registration = models.OneToOneField(
        Registration,
        on_delete=models.CASCADE,
        related_name="check_in",
    )
    check_in_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-check_in_at"]

    def __str__(self):
        return self.registration.email
