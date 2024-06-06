from django.contrib import admin

from core.models import Hymnary, HymnarySong, Tag

# Register your models here.
admin.site.register(Hymnary)
admin.site.register(HymnarySong)
admin.site.register(Tag)
