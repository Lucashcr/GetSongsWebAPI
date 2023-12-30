from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from django.http import JsonResponse
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Artist, Category, Song
from .serializers import CategorySerializer, ArtistSerializer, SongSerializer


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


class RegisterUserView(APIView):
    permission_classes = []

    def post(self, request):
        new_user = User(
            username=request.data.get('username'),
            email=request.data.get('email'),
            first_name=request.data.get('first_name'),
            last_name=request.data.get('last_name'),
        )

        try:
            new_user.validate_unique()
            new_user.set_password(request.data.get('password'))
            new_user.clean_fields()
        except ValidationError as e:
            return JsonResponse(e.messages, status=400, safe=False)
        else:
            new_user.save()
            return JsonResponse(
                model_to_dict(
                    new_user, ['username', 'email', 'first_name', 'last_name']
                ),
                status=201
            )


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ArtistViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    serializer_class = ArtistSerializer

    def get_queryset(self):
        queryset = Artist.objects.all()
        category_id = self.request.query_params.get('category_id', None)

        if category_id:
            queryset = (
                queryset
                .filter(song__category_id=category_id)
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
