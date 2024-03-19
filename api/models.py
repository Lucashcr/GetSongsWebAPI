import re
from bs4 import BeautifulSoup
from httpx import get

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from meilisearch import Client


from mysite.settings import MEILI_SETTINGS


meili_client = Client(**MEILI_SETTINGS)
meili_index = meili_client.index('songs')

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


@receiver(post_save, sender=Song)
def update_index(sender, instance, **kwargs):
    from api.serializers import SongSerializerFull
    meili_index.add_documents(SongSerializerFull(instance).data, primary_key='id')