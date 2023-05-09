import re
from bs4 import BeautifulSoup

from django.db import models

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

    def __str__(self) -> str:
        return f'{self.name} - {self.artist.name}'

    def get_lyrics(self, client):
        soup = BeautifulSoup(client.get(self.lyrics_url).text, 'html.parser')

        lyrics = re.findall(
            r'<p>(.*?)</p>', str(soup.find('div', {'class': 'cnt-letra'})))
        for i in range(len(lyrics)):
            lyrics[i] = lyrics[i].replace('<br>', '<br/>')
            lyrics[i] = lyrics[i].replace('</br>', '<br/>')

        return lyrics
