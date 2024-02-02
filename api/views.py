from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.views import APIView

from .models import Artist, Category, Song
from .serializers import CategorySerializer, ArtistSerializer, SongSerializer


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
    serializer_class = SongSerializer

    def get_queryset(self):
        queryset = Song.objects.all()
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
        songs = Song.search(query)

        hits = songs["hits"]
        for hit in hits:
            hit["artist"] = ArtistSerializer(hit.pop("artist_id")).data
            hit["category"] = CategorySerializer(hit.pop("category_id")).data
            
        return JsonResponse(SongSerializer(hits, many=True).data, safe=False)
        # return JsonResponse(songs)