from django.forms import model_to_dict
from django.views.generic import TemplateView
from django.http import JsonResponse

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *

# Create your views here.


class GetCurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = model_to_dict(request.user, [
            'username',
            'email',
            'first_name',
            'last_name',
        ])
        data['full_name'] = f"{data['first_name']} {data['last_name']}"
        return JsonResponse(data)


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

        slug = kwargs.pop('slug', None)
        if slug is not None:
            by_artist = Song.objects.filter(artist__slug=slug)
            by_category = Song.objects.filter(category__slug=slug)

            if by_artist.count() > 0:
                context_data['collection'] = by_artist
                context_data['filtered'] = Artist.objects.get(slug=slug).name
            elif by_category.count() > 0:
                context_data['collection'] = by_category
                context_data['filtered'] = Category.objects.get(slug=slug).name

        context_data['datatype'] = 'músicas'
        return context_data
