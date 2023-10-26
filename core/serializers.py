from rest_framework.serializers import ModelSerializer

from core.models import Hymnary
from api.serializers import SongSerializer

class HymnarySerializer(ModelSerializer):
    songs = SongSerializer(many=True)
    class Meta:
        model = Hymnary
        fields = '__all__'