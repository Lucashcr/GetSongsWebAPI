from typing import Any, Iterable

from meilisearch import Client
from meilisearch.errors import MeilisearchApiError

from mysite.settings import MEILI_SETTINGS

from api.serializers import SongSerializerFull
from api.models import Song


meili_client = Client(**MEILI_SETTINGS)
meili_index = meili_client.index('songs')


def search(query: str, **opt_params) -> Iterable[dict[str, Any]]:
    return meili_index.search(query, opt_params)


def populate() -> None:
    try:
        meili_client.get_index('songs')
    except MeilisearchApiError:
        meili_client.create_index('songs', {'primaryKey': 'id'})
        meili_index.update_filterable_attributes(['artist.id', 'category.id'])
    
    songs = Song.objects.select_related('artist', 'category').all()
    index = meili_index
    
    count_db = songs.count()
    count_index = index.get_stats().number_of_documents
    
    data = SongSerializerFull(songs, many=True).data
    index.add_documents(data, primary_key='id')
    
    count_index_new = index.get_stats().number_of_documents
    return count_index_new, count_index_new - count_index, count_db - count_index
    

def rebuild() -> None:
    try:
        meili_client.get_index('songs')
    except MeilisearchApiError:
        meili_client.create_index('songs', {'primaryKey': 'id'})
        meili_index.update_filterable_attributes(['artist.id', 'category.id'])
        
    meili_index.delete_all_documents()
    meili_index.update_filterable_attributes(['artist.id', 'category.id'])
    return populate()