from django.db import models

class Attendee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    location = models.CharField(max_length=150)

class Registration(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    class Meta:
        unique_together = ("attendee", "event")

from .repositories import AttendeeManager, EventManager, RegistrationManager
Attendee.add_to_class("objects", AttendeeManager())
Event.add_to_class("objects", EventManager())
Registration.add_to_class("objects", RegistrationManager())