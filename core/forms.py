from django import forms

from api.models import *

__all__ = ['AddSongForm']

class AddSongForm(forms.Form):
    category = forms.ModelChoiceField(Category.objects, label='Categoria')
    artist = forms.ModelChoiceField(Artist.objects, label='Artista')
    song = forms.ModelChoiceField(Song.objects, label='Música')
    # category = forms.ChoiceField(choices=map(lambda x: (x.slug, x.name), Categories.objects.all()))
    # artists = forms.ChoiceField(choices=map(lambda x: (x.slug, x.name), Artists.objects.all()))
