from .common import WishlistSerializer
from artworks.serializers.common import ArtworkSerializer
from authentication.serializers import UserSerializer

class PopulatedWishlistSerializer(WishlistSerializer):
    user = UserSerializer()
    artwork = ArtworkSerializer()

    