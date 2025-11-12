from django.db import models
from .models import Attendee, Event, Registration

class AttendeeManager(models.Manager):
    def by_email(self, email):
        return self.filter(email__iexact=email)

class EventManager(models.Manager):
    def upcoming(self):
        return self.order_by("date")

class RegistrationManager(models.Manager):
    def for_attendee(self, attendee_id):
        return self.filter(attendee_id=attendee_id)