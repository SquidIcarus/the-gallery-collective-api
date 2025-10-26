from .common import EventSerializer
from artists.serializers.populated import PopulatedArtistSerializer

class PopulatedEventSerializer(EventSerializer):
    artist = PopulatedArtistSerializer()

    