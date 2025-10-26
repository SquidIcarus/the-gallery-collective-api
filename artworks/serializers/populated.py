from .common import ArtworkSerializer
from artists.serializers.populated import PopulatedArtistSerializer

class PopulatedArtworkSerializer(ArtworkSerializer):
    artist = PopulatedArtistSerializer()

