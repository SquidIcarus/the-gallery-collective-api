from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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
                status=status.HTTP_422_UNPORCESSABLE_ENTITY
            )