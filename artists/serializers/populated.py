from .common import ArtistSerializer
from authentication.serializers import UserSerializer

class PopulatedArtistSerializer(ArtistSerializer):
    user = UserSerializer()

    