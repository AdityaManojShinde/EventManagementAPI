from rest_framework.routers import DefaultRouter

from event_app.views import (
    CheckInView,
    EventView,
    RegistrationView,
    UserViewSet,
    EventOptionViewSet,
)

router = DefaultRouter()

router.register("events", EventView, basename="event")
router.register("registrations", RegistrationView, basename="registration")
router.register("check-ins", CheckInView, basename="check-in")
router.register("users", UserViewSet, basename="user")
router.register("event-options", EventOptionViewSet, basename="event-option")

urlpatterns = router.urls
