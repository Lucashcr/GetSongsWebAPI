import os
import json
from datetime import datetime

from django.core.mail import send_mail
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.http.response import FileResponse
from django.http import HttpRequest, JsonResponse

from build_doc.templates import SingleColumnTemplate, TwoColumnsTemplate

from api.models import *
from core.models import Hymnary
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
        hymnary_owner = Hymnary.objects.get(id=kwargs.get('hymnary_id')).owner
        if request.user == hymnary_owner:
            return super().get(request, *args, **kwargs)
        else:
            return redirect('/hymnary')


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
    file_path = os.path.join(file_name)

    if hymnary.template in ('single-column', 'each-song-by-page'):
        HymnaryTemplate = SingleColumnTemplate
    elif hymnary.template == 'two-columns':
        HymnaryTemplate = TwoColumnsTemplate

    doc = HymnaryTemplate(file_path, title=hymnary.title)
    doc.insert_heading(hymnary.title, 'heading1-centered')
    for item in hymnary.hymnary_songs.all():
        song = item.song
        preview_url = song.preview_url.replace('embed/', '')
        doc.insert_heading(
            song.category.name) if hymnary.print_category else None
        doc.insert_heading_link(
            f'{song.name} - {song.artist}', preview_url, 'heading2')
        for p in song.get_lyrics():
            doc.insert_paragraph(p)
        if hymnary.template == 'each-song-by-page':
            doc.add_new_page()
    doc.build()
    as_attachment = bool(request.GET.get('as_attachment'))
    response = FileResponse(open(file_path, 'rb'),
                            as_attachment=as_attachment, filename=file_name)

    os.remove(file_path)

    return response


def save_hymnary(request: HttpRequest, hymnary_id):
    try:
        hymnary = Hymnary.objects.get(id=hymnary_id)

        if request.method == 'PUT' and hymnary.owner == request.user:
            request_body = json.loads(request.body)
            hymnary.print_category = request_body['print_category']
            hymnary.template = request_body['template']

            hymnary.songs.clear()
            for i, song_id in enumerate(request_body['songs_id']):
                hymnary.songs.add(
                    Song.objects.get(id=song_id),
                    through_defaults={'order': i + 1}
                )
    except Exception as e:
        print(e)
        alert = 'Ops, tivemos um problema em salvar seu hinário! Tente novamente mais tarde ou entre em contato.'
    else:
        hymnary.save()
        alert = 'Hinário salvo com sucesso'

    return JsonResponse({'alert': alert})
