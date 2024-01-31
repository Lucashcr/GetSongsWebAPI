from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient

from api.models import Artist, Category, Song
from core.models import Hymnary, HymnarySong


class TestHymnaryViewSet(APITestCase):
    client_class = APIClient

    def setUp(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        token = self.client.post(
            '/user/token/',
            {'username': 'testuser', 'password': 'testpassword'}
        ).json()['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        self.song = Song.objects.create(
            name='Test Song 1',
            slug='test-song-1',
            artist=Artist.objects.create(
                name='Test Artist 1',
                slug='test-artist-1',
            ),
            category=Category.objects.create(
                name='Test Category',
                slug='test-category'
            ),
            lyrics='Test Lyrics 1'
        )

        self.another_song = Song.objects.create(
            name='Test Song 2',
            slug='test-song-2',
            artist=Artist.objects.create(
                name='Test Artist 2',
                slug='test-artist-2',
            ),
            category=Category.objects.create(
                name='Test Category',
                slug='test-category'
            ),
            lyrics='Test Lyrics 2'
        )

        self.hymnary = Hymnary.objects.create(
            title='Test Hymnary',
            owner=user,
        )
        self.hymnarysong = HymnarySong.objects.create(
            hymnary=self.hymnary,
            song=self.song,
            order=1
        )

        another_user = User.objects.create_user(
            username='anotheruser',
            password='anotherpassword'
        )

        self.another_hymnary = Hymnary.objects.create(
            title='Another Test Hymnary',
            owner=another_user,
        )
        self.another_hymnarysong = HymnarySong.objects.create(
            hymnary=self.another_hymnary,
            song=self.song,
            order=1
        )

    def test_should_create_hymnarysong(self):
        hymnarysong_data = {
            'hymnary': self.hymnary.id,
            'song': self.another_song.id,
            'order': 2
        }

        response = self.client.post('/api/hymnarysong/', hymnarysong_data)

        self.assertEqual(response.status_code, 201)

    def test_should_not_create_hymnarysong_to_another_user(self):
        hymnarysong_data = {
            'hymnary': self.another_hymnary.id,
            'song': self.another_song.id,
            'order': 2
        }

        response = self.client.post('/api/hymnarysong/', hymnarysong_data)

        self.assertEqual(response.status_code, 400)

    def test_should_read_hymnarysong(self):
        response = self.client.get(f'/api/hymnarysong/{self.hymnarysong.id}/')

        self.assertEqual(response.status_code, 200)

    def test_should_not_read_hymnarysong_from_another_user(self):

        response = self.client.get(
            f'/api/hymnarysong/{self.another_hymnarysong.id}/'
        )

        self.assertEqual(response.status_code, 404)

    def test_should_update_hymnarysong(self):
        hymnarysong_data = {
            'hymnary': self.hymnary.id,
            'song': self.song.id,
            'order': 2
        }

        response = self.client.put(
            f'/api/hymnarysong/{self.hymnarysong.id}/', hymnarysong_data
        )

        self.assertEqual(response.status_code, 200)

    def test_should_not_update_hymnarysong_from_another_user(self):
        hymnarysong_data = {
            'hymnary': self.another_hymnary.id,
            'song': self.song.id,
            'order': 2
        }

        response = self.client.put(
            f'/api/hymnarysong/{self.another_hymnarysong.id}/',
            hymnarysong_data
        )

        self.assertEqual(response.status_code, 404)

    def test_should_delete_hymnarysong(self):
        response = self.client.delete(
            f'/api/hymnarysong/{self.hymnarysong.id}/'
        )

        self.assertEqual(response.status_code, 204)

    def test_should_not_delete_hymnarysong_from_another_user(self):
        response = self.client.delete(
            f'/api/hymnarysong/{self.another_hymnarysong.id}/'
        )

        self.assertEqual(response.status_code, 404)

    def test_should_set_hymnary_updated_to_true(self):
        response = self.client.post(
            f'/api/hymnarysong/', {
                'hymnary': self.hymnary.id,
                'song': self.another_song.id,
                'order': 2
            }
        )

        self.assertEqual(response.status_code, 201)
        hs = HymnarySong.objects.get(id=response.json()['id'])
        self.assertEqual(hs.hymnary.updated, True)
