import re
from typing import Any, Iterable, Optional
from bs4 import BeautifulSoup
from httpx import get

from django.db import models
from meilisearch import Client

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
        songs = cls.objects.select_related('artist', 'category').all()
        index = cls.meili_index
        
        count_db = songs.count()
        count_index = index.get_stats().number_of_documents
        
        index.add_documents(list(songs.values()), primary_key='id')
        
        count_index_new = index.get_stats().number_of_documents
        return count_index_new, count_index_new - count_index, count_db - count_index