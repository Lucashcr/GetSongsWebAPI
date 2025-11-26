import json
import os, re
from datetime import datetime

from django.http.response import FileResponse
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
    JsonResponse,
)

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from api.serializers import SongSerializer
from build_doc.templates import SingleColumnTemplate, TwoColumnsTemplate
from build_doc.styles import *

from api.models import *
from core.models import Hymnary, HymnarySong, Tag
from core.serializers import HymnarySerializer, TagSerializer
from core.pagination import HymnaryListPageNumberPagination

# Create your views here.
# ------------------------------------------------------------------------------------------------------
# API VIEWS


class HymnaryViewSet(ModelViewSet):
    serializer_class = HymnarySerializer
    pagination_class = HymnaryListPageNumberPagination

    def get_queryset(self):
        params = self.request.query_params
        queryset = Hymnary.objects.filter(owner=self.request.user)

        search = params.get("search")
        if search:
            queryset = queryset.filter(title__icontains=search)

        date_filter = params.get("dateFilter")
        from_date = params.get("fromDate")
        to_date = params.get("toDate")

        if date_filter:
            if date_filter not in ["created_at", "updated_at"]:
                raise ValueError("Parâmetro dateFilter inválido")

            if from_date:
                queryset = queryset.filter(**{f"{date_filter}__gte": from_date})

            if to_date:
                queryset = queryset.filter(**{f"{date_filter}__lte": to_date})

        tags = params.get("tags")
        if tags:
            tags = json.loads(tags)
            for tag in tags:
                queryset = queryset.filter(tags__id=tag)

        return queryset.order_by("-updated_at")

    def create(self, request, *args, **kwargs):
        request.data["owner"] = request.user.id
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=["get"])
    def list_titles(self, request):
        hymnary_names = Hymnary.objects.filter(owner=request.user).values_list(
            "title", flat=True
        )
        return JsonResponse(list(hymnary_names), safe=False)

    @action(detail=True, methods=["get"])
    def export(self, request, pk):
        try:
            hymnary = Hymnary.objects.get(id=pk, owner=request.user)
        except:
            return HttpResponseNotFound("Hinário não encontrado")

        if not hymnary.updated and os.path.exists(hymnary.file.path):
            return FileResponse(
                hymnary.file, as_attachment=False, filename=hymnary.file.name
            )

        owner_folder = f"{request.user.username}"
        if not os.path.exists(owner_folder):
            os.makedirs(owner_folder)

        safe_hymnary_title = re.sub(r"[^a-zA-Z0-9]", "_", hymnary.title)
        file_name = f"{owner_folder}/{safe_hymnary_title}_{datetime.now().strftime('%d_%m_%Y-%H_%M')}.pdf"
        file_path = os.path.join(file_name)

        if hymnary.template in ("single-column", "each-song-by-page"):
            HymnaryTemplate = SingleColumnTemplate
        elif hymnary.template == "two-columns":
            HymnaryTemplate = TwoColumnsTemplate
        else:
            return HttpResponseBadRequest("Template inválido")

        doc = HymnaryTemplate(file_path, title=hymnary.title)
        doc.insert_heading(hymnary.title, CENTERED_HEADING)
        for item in hymnary.hymnarysongs.all().order_by("order"):
            song = item.song
            preview_url = song.preview_url.replace("www.youtube.com/embed", "youtu.be")
            if hymnary.print_category:
                doc.insert_heading(song.category.name)
                heading_style = HEADING_2
            else:
                heading_style = HEADING_1

            doc.insert_heading_link(
                f"{song.name}<br/>{song.artist}", preview_url, heading_style
            )

            doc.insert_paragraph(song.lyrics)

            if hymnary.template == "each-song-by-page":
                doc.add_new_page()

        doc.build()

        if hymnary.file:
            hymnary.file.delete()

        response = FileResponse(
            open(file_path, "rb"), as_attachment=False, filename=file_name
        )

        hymnary.file.save(file_name, open(file_path, "rb"))

        os.remove(file_path)

        hymnary.updated = False
        hymnary.save()

        return response

    @action(detail=True, methods=["post"], url_path=r"add/(?P<song>\d+)")
    def add(self, request, pk, song):
        try:
            hymnary = Hymnary.objects.get(id=pk, owner=request.user)
        except:
            return HttpResponseNotFound("Hinário não encontrado")

        if not song:
            return HttpResponseBadRequest("Atributo song não enviado")

        if not Song.objects.filter(id=song).exists():
            return HttpResponseNotFound("Música não encontrada")

        try:
            hymnarysong = HymnarySong.objects.create(
                hymnary=hymnary, song_id=song, order=hymnary.hymnarysongs.count() + 1
            )
        except:
            return HttpResponseForbidden("Está música já foi adicionada a este hinário")

        hymnary.updated = True
        hymnary.save()

        return JsonResponse(SongSerializer(hymnarysong.song).data, safe=False)

    @action(detail=True, methods=["delete"], url_path="remove/(?P<song>\d+)")
    def remove(self, request, pk, song):
        try:
            hymnary = Hymnary.objects.get(id=pk, owner=request.user)
        except:
            return HttpResponseNotFound("Hinário não encontrado")
        else:
            if not song:
                return HttpResponseBadRequest("Atributo song não enviado")

            hymnarysong = HymnarySong.objects.get(hymnary=hymnary, song_id=song)
            hymnarysong.delete()

            hymnary.updated = True
            hymnary.save()

            return JsonResponse(SongSerializer(hymnarysong.song).data)

    @action(detail=True, methods=["post"])
    def reorder(self, request, pk):
        try:
            hymnary = Hymnary.objects.get(id=pk, owner=request.user)
        except:
            return HttpResponseNotFound("Hinário não encontrado")
        else:
            songs = request.data.get("songs")
            if not songs:
                return HttpResponseBadRequest("Atributo songs não enviado")

            new_songs = [
                HymnarySong.objects.get(song_id=song, hymnary=hymnary) for song in songs
            ]
            for i, song in enumerate(new_songs):
                song.order = i + 1

            HymnarySong.objects.bulk_update(new_songs, ["order"])

            hymnary.updated = True
            hymnary.save()

            return HttpResponse("Ordem das músicas atualizada com sucesso")

    @action(detail=True, methods=["post"], url_path="add_tag/(?P<tag_id>\d+)")
    def add_tag(self, request, pk, tag_id):
        try:
            hymnary = Hymnary.objects.get(id=pk, owner=request.user)
        except:
            return HttpResponseNotFound("Hinário não encontrado")
        else:
            if not tag_id:
                return HttpResponseBadRequest("Atributo tag não enviado")

            tag = Tag.objects.get(id=tag_id)
            hymnary.tags.add(tag)

            return JsonResponse(HymnarySerializer(hymnary).data["tags"], safe=False)

    @action(detail=True, methods=["delete"], url_path="remove_tag/(?P<tag_id>\d+)")
    def remove_tag(self, request, pk, tag_id):
        try:
            hymnary = Hymnary.objects.get(id=pk, owner=request.user)
        except:
            return HttpResponseNotFound("Hinário não encontrado")
        else:
            if not tag_id:
                return HttpResponseBadRequest("Atributo tag não enviado")

            tag = Tag.objects.get(id=tag_id)
            hymnary.tags.remove(tag)

            return JsonResponse(HymnarySerializer(hymnary).data["tags"], safe=False)


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer

    def get_queryset(self):
        queryset = Tag.objects.filter(owner=self.request.user)
        if self.request.query_params.get("mine"):
            return queryset.order_by("name")

        queryset |= Tag.objects.filter(owner=None)

        hymnary = self.request.query_params.get("hymnary")
        if hymnary:
            queryset = queryset.filter(hymnary__id=hymnary)

        owner = self.request.query_params.get("owner")
        if owner:
            queryset = queryset.filter(owner__id=owner)

        return queryset.order_by("name")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
