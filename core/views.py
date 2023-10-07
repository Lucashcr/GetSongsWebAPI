import os
import json
from datetime import datetime

from django.core.mail import send_mail
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.forms import model_to_dict
from django.http.response import FileResponse
from django.http import (
    HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseBadRequest,
    HttpResponseNotAllowed, HttpResponseNotFound, JsonResponse
)

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view

from build_doc.templates import SingleColumnTemplate, TwoColumnsTemplate
from build_doc.styles import *

from api.models import *
from core.models import Hymnary, HymnarySong
from mysite.settings import BASE_DIR, TIME_ZONE


# Create your views here.
class HomeView(TemplateView):
    template_name = "pages/index.html"


class AboutView(TemplateView):
    template_name = "pages/about.html"


class ThanksContactView(TemplateView):
    template_name = "pages/thanks_contact.html"


class ContactView(TemplateView):
    template_name = "pages/contact.html"

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message').split('\n')

        with open(BASE_DIR/'core'/'templates'/'email'/'contact.html', 'r') as f:
            html_message = f.read() % (
                name, email,
                datetime.now(TIME_ZONE).strftime('%d/%m/%Y %H:%M:%S'),
                ''.join(f'<p>{p}</p>' for p in message)
            )

        send_mail(
            f'{name} - Contato via GetSongs', '', None,
            [email, 'lucash.rocha@hotmail.com'],
            html_message=html_message
        )

        return redirect('/thanks-contact')


class ListHymnaries(TemplateView):
    template_name = "pages/list_hymnaries.html"

    def get_context_data(self):
        context = super().get_context_data()
        context['hymnaries'] = Hymnary.objects.filter(owner=self.request.user)
        return context


class TemplateHymnaryView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            context["hymnary"] = Hymnary.objects.get(id=kwargs['hymnary_id'])
            context["categories"] = Category.objects.all()
        except:
            ...

        return context

    def get(self, request, *args, **kwargs):
        try:
            hymnary = Hymnary.objects.get(
                id=kwargs.get('hymnary_id'),
                owner=request.user
            )
            return super().get(request, *args, **kwargs)
        except:
            return HttpResponseNotFound('Hinário não encontrado')


class ShowHymnary(TemplateHymnaryView):
    template_name = "pages/show_hymnary.html"


class EditHymnary(TemplateHymnaryView):
    template_name = 'pages/edit_hymnary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["templates"] = Hymnary.TEMPLATE_CHOICES
        return context


class DeleteHymnary(TemplateHymnaryView):
    template_name = 'pages/delete_hymnary.html'

    def post(self, request, *args, **kwargs):
        try:
            hymnary = Hymnary.objects.get(
                id=kwargs.get('hymnary_id'),
                owner=request.user
            )
            hymnary.delete()
        except:
            return HttpResponseNotFound('Hinário não encontrado')


# ------------------------------------------------------------------------------------------------------
# API VIEWS

class ListHymanariesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        hymnaries = Hymnary.objects.filter(owner=request.user)
        return JsonResponse([
            {
                'id': hymnary.id,
                'title': hymnary.title,
                'created_at': hymnary.created_at,
            }
            for hymnary in hymnaries
        ], safe=False)

    def post(self, request):
        if not (hymnary_title := request.data.get('title')):
            return HttpResponseBadRequest('Missing hymnary title')
            
        hymnary = Hymnary.objects.create(
            title=hymnary_title,
            owner=request.user
        )

        return JsonResponse(model_to_dict(hymnary))
            


class DetailHymnaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, hymnary_id):
        hymnary = Hymnary.objects.get(id=hymnary_id, owner=request.user)
        return JsonResponse({
            'id': hymnary.id,
            'title': hymnary.title,
            'created_at': hymnary.created_at,
            'updated_at': hymnary.updated_at,
            'print_category': hymnary.print_category,
            'template': hymnary.template,
            'songs': [
                {
                    'id': song.id,
                    'name': song.name,
                    'artist': song.artist.name,
                    'category': song.category.name,
                    'preview_url': song.preview_url,
                }
                for song in hymnary.songs.all().order_by('song_hymnaries__order')
            ]
        })

    def delete(self, request, hymnary_id):
        try:
            hymnary = Hymnary.objects.get(id=hymnary_id, owner=request.user)
        except:
            return HttpResponseNotFound('Hinário não encontrado')
        else:
            hymnary.delete()
            return HttpResponse('Hinário deletado com sucesso')
        
    def put(self, request, hymnary_id):
        try:
            hymnary = Hymnary.objects.get(id=hymnary_id, owner=request.user)
        except:
            return HttpResponseNotFound('Hinário não encontrado')
        else:
            hymnary.print_category = request.data['print_category']
            hymnary.template = request.data['template']
            hymnary.title = request.data['title']
            hymnary.save()

            return HttpResponse('Hinário atualizado com sucesso')
        

class AddSongToHymnaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, hymnary_id):
        try:
            hymnary = Hymnary.objects.get(id=hymnary_id, owner=request.user)
        except:
            return HttpResponseNotFound('Hinário não encontrado')
        else:
            song_id = request.data.get('song_id')
            if not song_id:
                return HttpResponseBadRequest('Missing song_id')

            try:
                song = Song.objects.prefetch_related('artist', 'category').get(id=song_id)
            except:
                return HttpResponseNotFound('Música não encontrada')

            HymnarySong.objects.create(
                hymnary=hymnary,
                song=song,
                order=hymnary.songs.count() + 1
            )

            return JsonResponse({
                'id': song.id,
                'name': song.name,
                'artist': song.artist.name,
                'category': song.category.name,
                'preview_url': song.preview_url
            })

# ------------------------------------------------------------------------------------------------------
# FUNCTION BASED VIEWS


def new_hymnary(request, hymnary_name):
    new_hymnary = Hymnary(
        title=hymnary_name,
        owner=request.user
    )
    new_hymnary.save()
    return redirect(f'/hymnary/{new_hymnary.id}/edit')


def export_hymnary(request, hymnary_id):
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
    for item in hymnary.hymnary_songs.all():
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
    as_attachment = bool(request.GET.get('as_attachment'))
    response = FileResponse(
        open(file_path, 'rb'),
        as_attachment=as_attachment,
        filename=file_name
    )

    hymnary.file.save(file_name, open(file_path, 'rb'))

    os.remove(file_path)

    return response


def save_hymnary(request: HttpRequest, hymnary_id):
    try:
        hymnary = Hymnary.objects.get(
            id=hymnary_id,
            owner=request.user
        )

        if request.method != 'PUT':
            return HttpResponseNotAllowed('Método não permitido')

        request_body = json.loads(request.body)
        hymnary.print_category = request_body['print_category']
        hymnary.template = request_body['template']
        hymnary.title = request_body['new_title']

        hymnary.songs.clear()
        for i, song_id in enumerate(request_body['songs_id']):
            hymnary.songs.add(
                Song.objects.get(id=song_id),
                through_defaults={'order': i + 1}
            )
    except Exception as e:
        alert = 'Ops, tivemos um problema em salvar seu hinário! Tente novamente mais tarde ou entre em contato.'
        error = e.args[0]
        print(e)
        status = 500
    else:
        hymnary.save()
        alert = 'Hinário salvo com sucesso'
        error = None
        status = 200

    return JsonResponse({'alert': alert, 'error': error, 'status': status})
