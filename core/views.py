import os
from datetime import datetime

from django.http.response import FileResponse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.serializers import SongSerializer
from build_doc.templates import SingleColumnTemplate, TwoColumnsTemplate
from build_doc.styles import *

from api.models import *
from core.models import Hymnary, HymnarySong
from core.serializers import HymnarySerializer, HymnarySongSerializer


# Create your views here.
# ------------------------------------------------------------------------------------------------------
# API VIEWS

class HymnaryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = HymnarySerializer

    def get_queryset(self):
        return Hymnary.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['owner'] = request.user.id
        return super().create(request, *args, **kwargs)
    
    @action(detail=True, methods=['get'])
    def export(self, request, pk):
        try:
            hymnary = Hymnary.objects.get(id=pk, owner=request.user)
        except:
            return HttpResponseNotFound('Hinário não encontrado')

        if not hymnary.updated and os.path.exists(hymnary.file.path):
            return FileResponse(hymnary.file, as_attachment=False, filename=hymnary.file.name)
        
        owner_folder = f'{request.user.username}'
        if not os.path.exists(owner_folder):
            os.makedirs(owner_folder)

        file_name = f'{owner_folder}/{hymnary.title}_{datetime.now().strftime("%d_%m_%Y-%H_%M")}.pdf'
        file_path = os.path.join(file_name)

        if hymnary.template in ('single-column', 'each-song-by-page'):
            HymnaryTemplate = SingleColumnTemplate
        elif hymnary.template == 'two-columns':
            HymnaryTemplate = TwoColumnsTemplate
        else:
            return HttpResponseBadRequest('Template inválido')

        doc = HymnaryTemplate(file_path, title=hymnary.title)
        doc.insert_heading(hymnary.title, CENTERED_HEADING)
        for item in hymnary.hymnarysongs.all().order_by('order'):
            song = item.song
            preview_url = song.preview_url.replace('www.youtube.com/embed', 'youtu.be')
            if hymnary.print_category:
                doc.insert_heading(song.category.name)
                heading_style = HEADING_2
            else:
                heading_style = HEADING_1

            doc.insert_heading_link(
                f'{song.name}<br/>{song.artist}', preview_url, heading_style
            )

            doc.insert_paragraph(song.lyrics)

            if hymnary.template == 'each-song-by-page':
                doc.add_new_page()

        doc.build()

        if hymnary.file:
            hymnary.file.delete()

        response = FileResponse(
            open(file_path, 'rb'),
            as_attachment=False,
            filename=file_name
        )

        hymnary.file.save(file_name, open(file_path, 'rb'))

        os.remove(file_path)

        hymnary.updated = False
        hymnary.save()

        return response
    
    @action(detail=True, methods=['post'], url_path='add/(?P<song>\d+)')
    def add(self, request, pk, song):
        try:
            hymnary = Hymnary.objects.get(id=pk, owner=request.user)
        except:
            return HttpResponseNotFound('Hinário não encontrado')
        else:
            if not song:
                return HttpResponseBadRequest('Atributo song não enviado')
            
            hymnarysong = HymnarySong.objects.create(
                hymnary=hymnary,
                song_id=song,
                order=hymnary.hymnarysongs.count() + 1
            )

            hymnary.updated = True
            hymnary.save()

            return JsonResponse(SongSerializer(hymnarysong.song).data, safe=False)
        
    @action(detail=True, methods=['delete'], url_path='remove/(?P<song>\d+)')
    def remove(self, request, pk, song):
        try:
            hymnary = Hymnary.objects.get(id=pk, owner=request.user)
        except:
            return HttpResponseNotFound('Hinário não encontrado')
        else:
            if not song:
                return HttpResponseBadRequest('Atributo song não enviado')
            
            hymnarysong = HymnarySong.objects.get(
                hymnary=hymnary,
                song_id=song
            )
            hymnarysong.delete()

            hymnary.updated = True
            hymnary.save()

            return JsonResponse(SongSerializer(hymnarysong.song).data)
    
    @action(detail=True, methods=['post'])
    def reorder(self, request, pk):
        try:
            hymnary = Hymnary.objects.get(id=pk, owner=request.user)
        except:
            return HttpResponseNotFound('Hinário não encontrado')
        else:
            songs = request.data.get('songs')
            if not songs:
                return HttpResponseBadRequest('Atributo songs não enviado')

            new_songs = [
                HymnarySong.objects.get(song_id=song, hymnary=hymnary)
                for song in songs
            ]
            for i, song in enumerate(new_songs):
                song.order = i + 1

            HymnarySong.objects.bulk_update(new_songs, ['order'])

            hymnary.updated = True
            hymnary.save()

            return HttpResponse('Ordem das músicas atualizada com sucesso')
