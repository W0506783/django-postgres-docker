import pytest
from datetime import date
from events.models import Event, Registration
from events.services import RegistrationService

pytestmark = pytest.mark.django_db

def test_register_success():
    event = Event.objects.create(title="Test", date=date.today(), location="Halifax")
    reg = RegistrationService().register("Alice", "alice@example.com", event.id)
    assert Registration.objects.count() == 1
    assert reg.attendee.email == "alice@example.com"