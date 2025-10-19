from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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
            