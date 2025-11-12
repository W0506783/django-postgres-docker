from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Event, Attendee, Registration
from .serializers import EventSerializer, AttendeeSerializer, RegistrationSerializer
from .services import RegistrationService

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

    @action(detail=False, methods=["post"])
    def register(self, request):
        try:
            reg = RegistrationService().register(
                request.data["name"], request.data["email"], request.data["event_id"]
            )
            return Response({"id": reg.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)