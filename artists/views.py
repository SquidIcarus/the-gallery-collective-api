from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Artist
from .serializers import ArtistSerializer

class ArtistListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request):
        artists = Artist.objects.all()
        serialized_artists = ArtistSerializer(artists, many=True)
        return Response(serialized_artists.data, status=status.HTTP_200_OK)

class ArtistDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)


    def get_artist(self, pk):
        try:
            return Artist.objects.get(pk=pk)
        except Artist.DoesNotExist:
            raise NotFound(detail="Can't find that artist")


    def get(self, _request, pk):
        artist = self.get_artist(pk=pk)
        serialized_artist = ArtistSerializer(artist)
        return Response(serialized_artist.data, status=status.HTTP_200_OK)

 


    

