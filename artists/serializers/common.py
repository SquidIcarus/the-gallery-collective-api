from rest_framework import serializers
from ..models import Artist

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('user', 'bio', 'website', 'instagram', 'profile_image', 'date_joined')