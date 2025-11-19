from django.contrib import admin

# Register your models here.
# events/admin.py

from django.contrib import admin
from .models import Event, Attendee, Registration

# Register your models here.
admin.site.register(Event)
admin.site.register(Attendee)
admin.site.register(Registration)