from django.contrib import admin
from event_app.models import Event, Registration, CheckIn


admin.site.register(Event)
admin.site.register(Registration)
admin.site.register(CheckIn)
