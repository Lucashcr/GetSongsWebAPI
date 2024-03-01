import re
from typing import Any, Iterable
from bs4 import BeautifulSoup
from httpx import get

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from meilisearch import Client
from meilisearch.errors import MeilisearchApiError

from mysite.settings import MEILI_SETTINGS

# Create your models here.


class Category(models.Model):
    name = models.CharField('Nome', max_length=32)
    slug = models.CharField('Slug', max_length=32)

    def __str__(self) -> str:
        return self.name


class Artist(models.Model):
    name = models.CharField('Nome', max_length=32)
    slug = models.CharField('Slug', max_length=32)

    def __str__(self) -> str:
        return self.name


class Song(models.Model):
    name = models.CharField('Nome', max_length=64)
    slug = models.CharField('Slug', max_length=64)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    lyrics_url = models.CharField('Link da letra', max_length=256)
    preview_url = models.CharField('Link do preview', max_length=256)
    lyrics = models.TextField('Letra', blank=True, auto_created=True)

    def __str__(self) -> str:
        return f'{self.name} - {self.artist.name}'

    def get_lyrics(self):
        soup = BeautifulSoup(get(self.lyrics_url).text, 'html.parser')

        lyrics = re.findall(
            r'<p>(.*?)</p>', str(soup.find('div', {'class': 'lyric-original'}))
        )

        for i in range(len(lyrics)):
            lyrics[i] = lyrics[i].replace('<br>', '<br/>')
            lyrics[i] = lyrics[i].replace('</br>', '<br/>')

        return '<br/><br/>'.join(lyrics)

    def save(self, *args, **kwargs) -> None:
        if not self.lyrics:
            self.lyrics = self.get_lyrics()
        super().save(*args, **kwargs)

    meili_client = Client(**MEILI_SETTINGS)
    meili_index = meili_client.index('songs')

    @classmethod
    def search(cls, query: str, **opt_params) -> Iterable[dict[str, Any]]:
        return cls.meili_index.search(query, opt_params)
    
    @classmethod
    def populate(cls) -> None:
        try:
            cls.meili_client.get_index('songs')
        except MeilisearchApiError:
            cls.meili_client.create_index('songs', {'primaryKey': 'id'})
            cls.meili_index.update_filterable_attributes(['artist.id', 'category.id'])
        
        songs = cls.objects.select_related('artist', 'category').all()
        index = cls.meili_index
        
        count_db = songs.count()
        count_index = index.get_stats().number_of_documents
        
        from api.serializers import SongSerializerFull
        data = SongSerializerFull(songs, many=True).data
        index.add_documents(data, primary_key='id')
        
        count_index_new = index.get_stats().number_of_documents
        return count_index_new, count_index_new - count_index, count_db - count_index
    
    @classmethod
    def rebuild(cls) -> None:
        try:
            cls.meili_client.get_index('songs')
        except MeilisearchApiError:
            cls.meili_client.create_index('songs', {'primaryKey': 'id'})
            cls.meili_index.update_filterable_attributes(['artist.id', 'category.id'])
            
        cls.meili_index.delete_all_documents()
        cls.meili_index.update_filterable_attributes(['artist.id', 'category.id'])
        return cls.populate()


@receiver(post_save, sender=Song)
def update_index(sender, instance, **kwargs):
    from api.serializers import SongSerializerFull
    instance.__class__.meili_index.add_documents(SongSerializerFull(instance).data, primary_key='id')