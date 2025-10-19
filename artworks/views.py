from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Artwork
from .serializers.common import ArtworkSerializer

class ArtworkListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, _request):
        artworks = Artwork.objects.all()
        serialized_artworks = ArtworkSerializer(artworks, many=True)
        return Response(serialized_artworks.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not hasattr(request.user, 'artist'):
            return Response(
                {'error': 'Only artists can upload artwork'},
                status=status.HTTP_403_FORBIDDEN
            )

        request.data['artist'] = request.user.artist.user_id

        artwork_to_add = ArtworkSerializer(data=request.data)
        try:
            artwork_to_add.is_valid(raise_exception=True)
            artwork_to_add.save()
            return Response(artwork_to_add.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                e.__dict__ if e.__dict__ else str(e),
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

class ArtworkDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_artwork(self, pk):
        try:
            return Artwork.objects.get(pk=pk)
        except Artwork.DoesNotExist:
            raise NotFound(detail="Can't find that artwork")

    def get(self, _request, pk):
        artwork = self.get_artwork(pk=pk)
        serialized_artwork = ArtworkSerializer(artwork)
        return Response(serialized_artwork.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        artwork_to_update = self.get_artwork(pk=pk)

        if artwork_to_update.artist.user != request.user:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        updated_artwork = ArtworkSerializer(
            artwork_to_update,
            data=request.data,
            partial=True
        )

        if updated_artwork.is_valid():
            updated_artwork.save()
            return Response(updated_artwork.data, status=status.HTTP_202_ACCEPTED)

        return Response(
            updated_artwork.errors,
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


    




