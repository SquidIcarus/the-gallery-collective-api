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