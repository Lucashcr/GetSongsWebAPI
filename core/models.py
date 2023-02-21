from django.db import models
from django.contrib.auth.models import User

from api.models import Song


class Hymnary(models.Model):
    title = models.CharField('Título', max_length=64)
    owner = models.ForeignKey(
        User,
        verbose_name='Proprietário',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    print_category = models.BooleanField('Imprimir categoria', default=True)
    songs = models.ManyToManyField(
        Song,
        verbose_name='Músicas',
        related_name='hymns',
        through='HymnarySong'
    )


class HymnarySong(models.Model):
    song = models.ForeignKey(
        Song,
        verbose_name='Música',
        on_delete=models.CASCADE,
        related_name='song_hymnaries'
    )
    hymnary = models.ForeignKey(
        Hymnary,
        verbose_name='Hinário',
        on_delete=models.CASCADE,
        related_name='hymnary_songs'
    )
    order = models.IntegerField('Ordem', unique=True)


# class Contact(models.Model):
#     name = models.CharField(max_length=64)
#     email = models.EmailField(max_length=128)
#     message = models.TextField()
