from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from django.db.models import Q

from event_app.models import Event, Registration, CheckIn
from event_app.serializers import (
    UserSerializer,
    EventSerializer,
    EventRegistrationSerializer,
    EventCheckInSerializer,
    EventOptionSerializer
)


class EventOptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.filter(
        end_at__gte=timezone.now(),
    ).only("id", "title")
    serializer_class = EventOptionSerializer
    permission_classes = [permissions.AllowAny]


class EventView(viewsets.ModelViewSet):
    """
    CRUD endpoint for Event. The read is public while other require admin permissions
    """

    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class RegistrationView(viewsets.ModelViewSet):
    """
    CRUS endpoint for Registration. create is public while other require admin permissions
    """

    queryset = Registration.objects.all()
    serializer_class = EventRegistrationSerializer

    def get_queryset(self):
        queryset = Registration.objects.all()

        event_id = self.request.query_params.get("event_id")
        search = self.request.query_params.get("search")

        if event_id:
            queryset = queryset.filter(event_id=event_id)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search)
            )

        return queryset

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class CheckInView(viewsets.ModelViewSet):
    """
    CRUD endpoint for CheckIn. require admin permissions
    """

    queryset = CheckIn.objects.all()
    serializer_class = EventCheckInSerializer
    permission_classes = [permissions.IsAdminUser]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
