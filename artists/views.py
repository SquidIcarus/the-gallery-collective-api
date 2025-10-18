from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Artist
from .serializers import ArtistSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ArtistListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    def get(self, _request):
        artists = Artist.objects.all()
        serialized_artists = ArtistSerializer(artists, many=True)
        return Response(serialized_artists.data, status=status.HTTP_200_OK)


