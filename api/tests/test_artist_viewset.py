from django.test import TestCase

from api.models import Artist, Category, Song


class TestArtistViewSet(TestCase):
    def setUp(self):
        category = Category.objects.create(
            id=1,
            name='Test Category',
            slug='test-category'
        )
        artist = Artist.objects.create(
            id=1,
            name='Test Artist 1',
            slug='test-artist-1',
        )
        Song.objects.create(
            id=1,
            name='Test Song 1',
            slug='test-song-1',
            artist=artist,
            category=category,
            lyrics='Test Lyrics 1'
        )

    def test_get_artists(self):
        response = self.client.get('/api/artist/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Artist 1')
        self.assertEqual(response.data[0]['slug'], 'test-artist-1')

    def test_get_artist(self):
        response = self.client.get('/api/artist/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test Artist 1')
        self.assertEqual(response.data['slug'], 'test-artist-1')

    def test_get_artist_not_found(self):
        response = self.client.get('/api/artist/999/')

        self.assertEqual(response.status_code, 404)

    def test_get_artists_by_category(self):
        response = self.client.get('/api/artist/?category_id=1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Artist 1')
        self.assertEqual(response.data[0]['slug'], 'test-artist-1')
