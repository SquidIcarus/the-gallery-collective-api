from .common import EventInterestSerializer
from events.serializers.common import EventSerializer
from authentication.serializers import UserSerializer

class PopulatedEventInterestSerializer(EventInterestSerializer):
    user = UserSerializer()
    event = EventSerializer()