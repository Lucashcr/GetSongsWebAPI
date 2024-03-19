from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from api.models import Song


class Hymnary(models.Model):
    title = models.CharField('Título', max_length=64)
    owner = models.ForeignKey(
        User,
        verbose_name='Proprietário',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    updated = models.BooleanField('Atualizado', default=True)
    print_category = models.BooleanField('Imprimir categoria', default=True)
    songs = models.ManyToManyField(
        Song,
        verbose_name='Músicas',
        related_name='hymns',
        through='HymnarySong'
    )
    TEMPLATE_CHOICES = (
        ('single-column', 'Uma coluna'),
        ('two-columns', 'Duas colunas'),
        ('each-song-by-page', 'Uma música por página')
    )
    template = models.CharField(
        'Modelo', max_length=32,
        choices=TEMPLATE_CHOICES,
        default='single-column'
    )
    file = models.FileField(
        'Arquivo',
        upload_to='hymnaries/',
        null=True
    )


class HymnarySong(models.Model):
    song = models.ForeignKey(
        Song,
        verbose_name='Música',
        on_delete=models.CASCADE,
        related_name='hymnarysongs'
    )
    hymnary = models.ForeignKey(
        Hymnary,
        verbose_name='Hinário',
        on_delete=models.CASCADE,
        related_name='hymnarysongs'
    )
    order = models.IntegerField('Ordem', unique=False)

    class Meta:
        unique_together = ('song', 'hymnary')


@receiver([post_save, post_delete], sender=HymnarySong)
def hymnary_song_post_save(sender, instance, **kwargs):
    hymnary = instance.hymnary
    hymnary.updated = True
    hymnary.save()
