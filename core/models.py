from django.db import models
from django.contrib.auth.models import User

from api.models import Song

# Create your models here.
class Hymnary(models.Model):
    title = models.CharField(max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    print_category = models.BooleanField(default=True)
    songs = models.ManyToManyField(Song, related_name='hymns', through='HymnarySong')

class HymnarySong(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='song_hymnaries')
    hymnary = models.ForeignKey(Hymnary, on_delete=models.CASCADE, related_name='hymnary_songs')
    order = models.IntegerField(unique=True)
