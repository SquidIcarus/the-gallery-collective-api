from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Artist
from artworks.models import Artwork
from events.models import Event
from artworks.serializers.populated import PopulatedArtworkSerializer
from events.serializers.populated import PopulatedEventSerializer
from .serializers.common import ArtistSerializer
from .serializers.populated import PopulatedArtistSerializer

class ArtistListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request):
        artists = Artist.objects.all()
        serialized_artists = PopulatedArtistSerializer(artists, many=True)
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
        serialized_artist = PopulatedArtistSerializer(artist)
        return Response(serialized_artist.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        artist_to_update = self.get_artist(pk=pk)
        
        if artist_to_update.user != request.user:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        updated_artist = ArtistSerializer(
            artist_to_update,
            data=request.data,
            partial=True
        )

        if updated_artist.is_valid():
            updated_artist.save()
            return Response(
                PopulatedArtistSerializer(artist_to_update).data,
                status=status.HTTP_202_ACCEPTED
            )

        return Response(
            updated_artist.errors,
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    def delete(self, request, pk):
        artist_to_delete = self.get_artist(pk=pk)

        if artist_to_delete.user != request.user:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        user_to_delete = artist_to_delete.user

        artist_to_delete.delete()
        user_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ArtistArtworksView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request, pk):
        try:
            artworks = Artwork.objects.filter(artist__user__id=pk)
            serialized_artworks = PopulatedArtworkSerializer(artworks, many=True)
            return Response(serialized_artworks.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )

class ArtistEventsView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request, pk):
        try:
            events = Event.objects.filter(artist__user__id=pk)
            serialized_events = PopulatedEventSerializer(events, many=True)
            return Response(serialized_events.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )



 


    

