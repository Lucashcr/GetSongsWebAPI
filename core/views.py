from datetime import datetime

from django.conf.global_settings import MEDIA_ROOT
from django.http import HttpRequest, HttpResponse
from django.http.response import FileResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView

import json, os
from api.models import *
from core.models import Hymnary

from build_doc.templates import SingleColumnTemplate, TwoColumnsTemplate
from build_doc import styles


# Create your views here.
class HomeView(TemplateView):
    template_name = "pages/index.html"


class AboutView(TemplateView):
    template_name = "pages/about.html"
    

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
        hymnary_owner = Hymnary.objects.get(id=kwargs.get('hymnary_id')).owner
        if request.user == hymnary_owner:
            return super().get(request, *args, **kwargs)
        else:
            return redirect('/hymnary')


class ShowHymnary(TemplateHymnaryView):
    template_name = "pages/show_hymnary.html"


class EditHymnary(TemplateHymnaryView):
    template_name = 'pages/edit_hymnary.html'


class DeleteHymnary(TemplateHymnaryView):
    template_name = 'pages/delete_hymnary.html'

    def post(self, request, *args, **kwargs):
        hymnary = Hymnary.objects.get(id=kwargs.get('hymnary_id'))
        if request.user == hymnary.owner:
            hymnary.delete()
        return redirect('/hymnary')


# ------------------------------------------------------------------------------------------------------

def new_hymnary(request, hymnary_name):
    new_hymnary = Hymnary(
        title=hymnary_name,
        owner=request.user
    )
    new_hymnary.save()
    return redirect(f'/hymnary/{new_hymnary.id}/edit')


def export_hymnary(request, hymnary_id):
    hymnary = Hymnary.objects.get(id=hymnary_id)

    file_name = f'{hymnary.title}_{datetime.now().strftime("%d_%m_%Y-%H_%M")}.pdf'
    file_path = os.path.join(MEDIA_ROOT, file_name)

    doc = SingleColumnTemplate(file_path, title=hymnary.title)
    doc.insert_heading(hymnary.title, 'heading1-centered')
    for item in hymnary.hymnary_songs.all():
        song = item.song
        preview_url = song.preview_url.replace('embed/', '')
        doc.insert_heading(song.category.name) if hymnary.print_category else None
        doc.insert_heading_link(f'{song.name} - {song.artist}', preview_url, 'heading2')
        for p in song.get_lyrics():
            doc.insert_paragraph(p)
    doc.build()
    as_attachment = bool(request.GET.get('as_attachment'))
    response = FileResponse(open(file_path, 'rb'), as_attachment=as_attachment, filename=file_name)
    
    os.remove(file_path)
    
    return response


# CRIAR VIEW PARA /hymnary/<id>/save
def save_hymnary(request: HttpRequest, hymnary_id):    
    hymnary = Hymnary.objects.get(id=hymnary_id)

    if request.method == 'PUT' and hymnary.owner == request.user:
        hymnary.songs.clear()

        request_body = json.loads(request.body)
        hymnary.print_category = request_body['print_category']

        for i, song_id in enumerate(request_body['songs_id']):
            hymnary.songs.add(
                Song.objects.get(id=song_id), 
                through_defaults={'order': i + 1}
            )

        hymnary.save()

    return HttpResponse()