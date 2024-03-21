from rest_framework.serializers import ModelSerializer, SerializerMethodField

from core.models import Hymnary, HymnarySong
from api.serializers import SongSerializer


class HymnarySerializer(ModelSerializer):
    songs = SerializerMethodField("get_songs")

    def get_songs(self, hymnary):
        songs = (
            hymnary.songs.all()
            .select_related("artist", "category")
            .order_by("hymnarysongs__order")
        )
        return SongSerializer(songs, many=True).data

    class Meta:
        model = Hymnary
        fields = "__all__"


class HymnarySongSerializer(ModelSerializer):
    song = SongSerializer()

    class Meta:
        model = HymnarySong
        fields = ["id", "song", "hymnary", "order"]
