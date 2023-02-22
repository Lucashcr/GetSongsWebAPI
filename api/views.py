from django.views.generic import TemplateView

from rest_framework import viewsets

from .models import *
from .serializers import *

# Create your views here.


class HomeView(TemplateView):
    template_name: str = "api/index.html"


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ShowCategoriesView(TemplateView):
    template_name = "api/show-api-data.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['collection'] = Category.objects.all()
        context_data['datatype'] = 'categorias'
        return context_data


class ArtistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class ShowArtistsView(TemplateView):
    template_name = "api/show-api-data.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['collection'] = Artist.objects.all()
        context_data['datatype'] = 'artistas'
        return context_data


class SongViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class ShowSongsView(TemplateView):
    template_name = "api/show-api-songs.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['collection'] = Song.objects.all()

        slug = kwargs.pop('slug', '')
        if slug != '':
            artists = Song.objects.filter(artist__slug=slug)
            categories = Song.objects.filter(categories__slug=slug)

            if artists.count() > 0:
                context_data['collection'] = artists
            elif categories.count() > 0:
                context_data['collection'] = categories

        context_data['datatype'] = 'músicas'
        return context_data
