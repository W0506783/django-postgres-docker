from django.db import transaction, IntegrityError
from .models import Attendee, Event, Registration

class RegistrationService:
    @transaction.atomic
    def register(self, name, email, event_id):
        attendee, _ = Attendee.objects.get_or_create(email=email, defaults={"name": name})
        event = Event.objects.get(id=event_id)
        try:
            reg = Registration.objects.create(attendee=attendee, event=event)
        except IntegrityError:
            raise ValueError("Attendee already registered for this event.")
        return reg