from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Event
from .serializers.common import EventSerializer

class EventListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, _request):
        events = Event.objects.all()
        serialized_events = EventSerializer(events, many=True)
        return Response(serialized_events.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not hasattr(request.user, 'artist'):
            return Response(
                {'error': 'Only artists can create events'},
                status=status.HTTP_403_FORBIDDEN
            )

        request.data['artist'] = request.user.artist.user_id
        event_to_add = EventSerializer(data=request.data)
        try:
            event_to_add.is_valid(raise_exception=True)
            event_to_add.save()
            return Response(event_to_add.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                e.__dict__ if e. __dict__ else str(e),
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

class EventDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_event(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise NotFound(detail="Can't find that event")

    def get(self, _request, pk):
        event = self.get_event(pk=pk)
        serialized_event = EventSerializer(event)
        return Response(serialized_event.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        event_to_update = self.get_event(pk=pk)

        if event_to_update.artist.user != request.user:
            return Response(
                {'error': 'Unauthorized'},
                status = status.HTTP_401_UNAUTHORIZED
            )

        updated_event = EventSerializer(
            event_to_update,
            data=request.data,
            partial=True
        )

        if updated_event.is_valid():
            updated_event.save()
            return Response(updated_event.data, status=status.HTTP_202_ACCEPTED)

        return Response(
            updated_event.errors,
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    def delete(self, request, pk):
        event_to_delete = self.get_event(pk=pk)

        if event_to_delete.artist.user != request.user:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        event_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

