from rest_framework import serializers

from .models import *


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class SongSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer()
    category = CategorySerializer()
    hymnarysong = serializers.SerializerMethodField('get_hymnarysong_id')

    def get_hymnarysong_id(self, song):
        if song.song_hymnaries.count() == 0:
            return None
        return song.song_hymnaries.first().id

    class Meta:
        model = Song
        fields = ['id', 'name', 'slug', 'artist', 'category',
                  'lyrics_url', 'preview_url', 'hymnarysong']
