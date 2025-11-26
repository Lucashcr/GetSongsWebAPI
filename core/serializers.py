from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)

from core.models import Hymnary, HymnarySong, Tag
from api.serializers import SongSerializer
from core.validators import validate_existing_name_tag


class TagSerializer(ModelSerializer):
    def validate(self, attrs):
        validate_existing_name_tag(attrs["name"], self.context["request"].user)
        return super().validate(attrs)

    class Meta:
        model = Tag
        fields = ["id", "name", "owner_id"]
        read_only_fields = ["id", "owner_id"]


class HymnarySerializer(ModelSerializer):
    songs = SerializerMethodField("get_songs")
    tags = TagSerializer(many=True, required=False)

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
