from rest_framework import serializers

from .models import Artist, Category, Song


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

    class Meta:
        model = Song
        fields = ['id', 'name', 'slug', 'artist', 'category',
                  'lyrics_url', 'preview_url', 'song_hymnaries']


class SongSerializerFull(serializers.ModelSerializer):
    artist = ArtistSerializer()
    category = CategorySerializer()

    class Meta:
        model = Song
        fields = '__all__'
