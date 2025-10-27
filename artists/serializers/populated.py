from .common import ArtistSerializer
from authentication.serializers import UserSerializer
from ..models import Artist

class PopulatedArtistSerializer(ArtistSerializer):
    user = UserSerializer()

    class Meta:
        model = Artist
        fields = ('user', 'bio', 'website', 'instagram', 'profile_image', 'date_joined')