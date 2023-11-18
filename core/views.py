import os
from datetime import datetime

from django.http.response import FileResponse
from django.http import HttpResponse, HttpResponseNotFound

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

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


class HymnarySongViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = HymnarySongSerializer
    queryset = HymnarySong.objects.all()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ExportHymnaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, hymnary_id):
        try:
            hymnary = Hymnary.objects.get(id=hymnary_id, owner=request.user)
        except:
            return HttpResponseNotFound('Hinário não encontrado')

        file_name = f'{hymnary.title}_{datetime.now().strftime("%d_%m_%Y-%H_%M")}.pdf'
        file_path = os.path.join(file_name)

        if hymnary.template in ('single-column', 'each-song-by-page'):
            HymnaryTemplate = SingleColumnTemplate
        elif hymnary.template == 'two-columns':
            HymnaryTemplate = TwoColumnsTemplate

        doc = HymnaryTemplate(file_path, title=hymnary.title)
        doc.insert_heading(hymnary.title, CENTERED_HEADING)
        for item in hymnary.hymnary_songs.all().order_by('order'):
            song = item.song
            preview_url = song.preview_url.replace('embed/', '')
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

        return response


class ReorderSongsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = HymnarySong.objects.all()

    def post(self, request, hymnary_id):
        try:
            hymnary = Hymnary.objects.get(id=hymnary_id, owner=request.user)
        except:
            return HttpResponseNotFound('Hinário não encontrado')
        else:
            songs = request.data['songs']

            new_songs = []
            for i, song in enumerate(songs):
                h = HymnarySong.objects.get(
                    song_id=song['id'], hymnary=hymnary)
                h.order = i + 1
                new_songs.append(h)

            HymnarySong.objects.bulk_update(new_songs, ['order'])

            return HttpResponse('Ordem das músicas atualizada com sucesso')
