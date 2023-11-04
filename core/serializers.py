from rest_framework.serializers import ModelSerializer, SerializerMethodField

from core.models import Hymnary, HymnarySong
from api.serializers import SongSerializer
import json


class HymnarySerializer(ModelSerializer):
    songs = SerializerMethodField('get_songs')

    def get_songs(self, hymnary):
        songs = hymnary.songs.all().order_by('song_hymnaries__order')
        return SongSerializer(songs, many=True).data

    class Meta:
        model = Hymnary
        fields = '__all__'


class HymnarySongSerializer(ModelSerializer):
    class Meta:
        model = HymnarySong
        fields = ['id', 'song', 'hymnary', 'order']
