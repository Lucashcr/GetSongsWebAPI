import os
import smtplib
from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.http.response import FileResponse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound

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

    def get_queryset(self):
        return HymnarySong.objects.filter(hymnary__owner=self.request.user)

    def create(self, request, *args, **kwargs):
        if not Hymnary.objects.filter(
            id=request.data['hymnary'],
            owner=request.user
        ).exists():
            return HttpResponseBadRequest('Hinário não encontrado')
        return super().create(request, *args, **kwargs)


class ExportHymnaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, hymnary_id):
        try:
            hymnary = Hymnary.objects.get(id=hymnary_id, owner=request.user)
        except:
            return HttpResponseNotFound('Hinário não encontrado')

        if not hymnary.updated:
            return FileResponse(hymnary.file, as_attachment=False, filename=hymnary.file.name)

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

        hymnary.updated = False
        hymnary.save()

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


class SendEmailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not all([
            request.data.get(fields)
            for fields in ('name', 'email', 'message')
        ]):
            return HttpResponseBadRequest('Dados inválidos')

        message = f'Usuário: {request.data["name"]}'
        message += f'\nEmail: {request.data["email"]}'
        message += f'\n\n{request.data["message"]}'

        response = send_mail(
            'Contato - GetSongs',
            message,
            settings.EMAIL_HOST_USER,
            ['lucash.rocha123@gmail.com'],
            fail_silently=False,
        )

        if response == 1:
            return HttpResponse('Email enviado com sucesso')

        return HttpResponse('Erro ao enviar email', status=500)
