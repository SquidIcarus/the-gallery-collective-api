from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from .models import Wishlist
from .serializers import WishlistSerializer
from artworks.models import Artwork

class WishlistView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        wishlists = Wishlist.objects.filter(user=request.user)
        serialized_wishlists = WishlistSerializer(wishlists, many=True)
        return Response(serialized_wishlists.data, status=status.HTTP_200_OK)

    def post(self, request):
        artwork_id = request.data.get('artwork_id')

        if not artwork_id:
            return Response(
                {'error': 'artwork_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            artwork = Artwork.objects.get(pk=artwork_id)
        except Artwork.DoesNotExist:
            raise NotFound(detail="Artwork not found")

        if Wishlist.objects.filter(user=request.user, artwork=artwork).exists():
            return Response(
                {'message': 'Artwork already in wishlist'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        wishlist_entry = Wishlist.objects.create(
            user=request.user,
            artwork=artwork
        )
        serialized_wishlist = WishlistSerializer(wishlist_entry)
        return Response(serialized_wishlist.data, statu=status.HTTP_201_CREATED)

class WishlistDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        try:
            wishlist_entry = Wishlist.objects.get(pk=pk, user=request.user)
        except Wishlist.DoesNotExist:
            raise NotFound(detail="Wishlist entry not found")

        wishlist_entry.delete()
        return Response(
            {'message': 'Removed from wishlist'},
            status=status.HTTP_204_NO_CONTENT
        )
