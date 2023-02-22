from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    sortable_by = ('id', 'name')
    list_display_links = ('name', )


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist')
    sortable_by = ('name', 'artist')
    search_fields = ('name', )
