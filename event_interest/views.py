from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from .models import EventInterest
from .serializers.common import EventInterestSerializer
from .serializers.populated import PopulatedEventInterestSerializer
from events.models import Event

class EventInterestView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        event_interests = EventInterest.objects.filter(user=request.user)
        serialized_interests = PopulatedEventInterestSerializer(event_interests, many=True)
        return Response(serialized_interests.data, status=status.HTTP_200_OK)

    def post(self, request):
        event_id = request.data.get('event_id')

        if not event_id:
            return Response(
                {'error': 'event_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            raise NotFound(detail="Event not found")

        if EventInterest.objects.filter(user=request.user, event=event).exists():
            return Response(
                {'message': 'Already RSVP\'d to this event'},
                status=status.HTTP_400_BAD_REQUEST
            )

        interest_entry = EventInterest.objects.create(
            user=request.user,
            event=event
        )

        serialized_interest = EventInterestSerializer(interest_entry)
        return Response(serialized_interest.data, status=status.HTTP_201_CREATED)

class EventInterestDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        try:
            interest_entry = EventInterest.objects.get(pk=pk, user=request.user)
        except EventInterest.DoesNotExist:
            raise NotFound(detail="Event interest not found")

        interest_entry.delete()
        return Response(
            {'message': 'RSVP cancelled'},
            status=status.HTTP_204_NO_CONTENT
        )