from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Event, User
from api.serializers import EventsSerializer
from django.utils.decorators import method_decorator
from core.utils.decorators import OrganizerOnly, AppUserOnly, OrganizerAndAppUserOnly


class EventListAPI(APIView):
    '''
    For getting all events created by the requester
    
    or all events that a user is a participant of
    '''
    permission_classes = (permissions.IsAuthenticated,)

    @method_decorator(OrganizerAndAppUserOnly)
    def get(self, request, *args, **kwargs):
        '''Uses get request to fetch all events'''
        user = request.user
        if user.role == "APP_USER":
            events = Event.objects.filter(participants=user).order_by("-id")
        elif user.role == "ORGANIZER":    
            events = Event.objects.filter(created_by=user).order_by("-id")
        else:
            events = []
        serializer = EventsSerializer(events, many=True)
        return Response({
            "events": serializer.data,
        }, status=status.HTTP_200_OK)


class CUDEventAPI(APIView):
    '''For Create, Update, Delete of events'''
    permission_classes = (permissions.IsAuthenticated,)

    @method_decorator(OrganizerOnly)
    def post(self, request, *args, **kwargs):
        '''Uses the post request to create a new event'''
        user = request.user
        name = request.data.get("name")
        date = request.data.get("date")
        # convert 2023-08-31 00:00:00.000 to 2023-08-31
        date = date.split(" ")[0]
        event = Event.objects.create(
            name=name,
            date=date,
            created_by=user
        )
        serializer = EventsSerializer(event, many=False)
        return Response({
            "event": serializer.data
        }, status=status.HTTP_201_CREATED)

    @method_decorator(OrganizerOnly)
    def put(self, request, *args, **kwargs):
        '''Uses the put request to update existing event'''
        user = request.user
        event_id = request.data.get("event_id")
        event = Event.objects.filter(event_id=event_id, created_by=user).first()  # noqa
        name = request.data.get("name")
        date = request.data.get("date")
        if event is not None:
            event.name = name
            event.date = date
            event.save()
            serializer = EventsSerializer(event, many=False)
            return Response({
                "event": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Event Not Found"
            }, status=status.HTTP_404_NOT_FOUND)

    @method_decorator(OrganizerOnly)
    def delete(self, request, *args, **kwargs):
        '''Uses the delete request to delete an event'''
        user = request.user
        event_id = request.data.get("event_id")
        event = Event.objects.filter(event_id=event_id, created_by=user).first()  # noqa
        if event is not None:
            event.delete()
            return Response({
                "message": "Event Deleted Successfully",
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Event Not Found"
            }, status=status.HTTP_404_NOT_FOUND)


class AddEventParticipantAPI(APIView):
    '''For users to register as participants of the event'''

    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(AppUserOnly)
    def post(self, request, *args, **kwargs):
        '''Uses the post request to add a participant to the event'''
        user = request.user
        event_id = request.data.get("event_id")
        event = Event.objects.filter(event_id=event_id).first()
        if event is not None:
            event.participants.add(user)
            event.save()
            serializer = EventsSerializer(event, many=False)
            return Response({
                "event": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Event Not Found"
            }, status=status.HTTP_404_NOT_FOUND)


class RemoveParticipant(APIView):
    '''Used by event organizers to remove participants from event participants'''

    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(OrganizerOnly)
    def post(self, request, *args, **kwargs):
        '''Uses delete request to remove participant from event participants'''
        event_id = request.data.get("event_id")
        event = Event.objects.filter(event_id=event_id).first()

        if not event:
            return Response({"message": "Event Not Found"}, status=status.HTTP_404_NOT_FOUND)

        participant_email = request.data.get("participant_email")
        participant = User.objects.filter(email=participant_email).first()

        if not participant:
            return Response({"message": "Participant Not Found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the participant is in the event participants
        if participant in event.participants.all():
            event.participants.remove(participant)
            return Response({"message": "Participant Removed Successfully"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"message": "User is Not a Participant of the Event"},
                            status=status.HTTP_400_BAD_REQUEST)
