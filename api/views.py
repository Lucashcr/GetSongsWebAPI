from django.http import JsonResponse

from rest_framework import viewsets
from rest_framework.views import APIView

from api.index import search

from .models import Artist, Category, Song
from .serializers import CategorySerializer, ArtistSerializer, SongSerializer, SongSerializerPrivate


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ArtistViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    serializer_class = ArtistSerializer

    def get_queryset(self):
        queryset = Artist.objects.all()
        category_id = self.request.query_params.get('category_id', 0)

        if int(category_id):
            queryset = (
                queryset
                .filter(song__category__id=category_id)
                .distinct()
            )

        return queryset.order_by('id')


class SongViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    serializer_class = SongSerializerPrivate

    def get_queryset(self):
        queryset = Song.objects.all().select_related('artist', 'category')
        artist_id = self.request.query_params.get('artist_id', 0)
        category_id = self.request.query_params.get('category_id', 0)

        if int(artist_id):
            queryset = queryset.filter(artist__id=artist_id)

        if int(category_id):
            queryset = queryset.filter(category__id=category_id)

        return queryset


class SongSearchAPIView(APIView):
    permission_classes = []
    
    def get(self, request):
        query = request.query_params.get('q', '')
        options = {}
        
        filter = []
        if request.query_params.get('artist_id'):
            filter.append(f'artist.id = {request.query_params["artist_id"]}')

        if request.query_params.get('category_id'):
            filter.append(f'category.id = {request.query_params["category_id"]}')
            
        if filter:
            options['filter'] = ' AND '.join(filter)
        
        songs = search(query, **options)

        return JsonResponse(SongSerializer(songs["hits"], many=True).data, safe=False)
