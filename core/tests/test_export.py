from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient

from api.models import Artist, Category, Song
from core.models import Hymnary


class TestExportHymnaryAPIView(APITestCase):
    client_class = APIClient

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.token = self.client.post(
            '/user/token/',
            {'username': 'testuser', 'password': 'testpassword'}
        ).json()['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.another_user = User.objects.create_user(
            username='anotheruser',
            password='anotherpassword'
        )

        song = Song.objects.create(
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

        self.hymnary = Hymnary.objects.create(
            title='Test Hymnary',
            owner=self.user,
        )
        self.hymnary.songs.add(song, through_defaults={'order': 1})

        self.another_hymnary = Hymnary.objects.create(
            title='Test Hymnary',
            owner=self.another_user,
        )
        self.another_hymnary.songs.add(song, through_defaults={'order': 1})

    def test_should_export_hymnary_updated(self):
        # Updated é iniciado como True quando o hinário é criado
        hymnary = Hymnary.objects.get(id=self.hymnary.id)
        self.assertEqual(hymnary.updated, True)

        response = self.client.get(f'/api/hymnary/{hymnary.id}/export')

        hymnary = Hymnary.objects.get(id=self.hymnary.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertEqual(hymnary.updated, False)

    def test_should_export_hymnary_not_updated(self):
        # Não há arquivo gerado inicialmente, logo é preciso exportar uma primeira vez
        # para gerar o arquivo a ser enviado na segunda requisição
        self.client.get(f'/api/hymnary/{self.hymnary.id}/export')

        hymnary = Hymnary.objects.get(id=self.hymnary.id)
        self.assertEqual(hymnary.updated, False)

        response = self.client.get(f'/api/hymnary/{hymnary.id}/export')

        hymnary = Hymnary.objects.get(id=self.hymnary.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertEqual(hymnary.updated, False)

    def test_should_not_export_hymnary_without_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='')

        response = self.client.get(f'/api/hymnary/{self.hymnary.id}/export')

        self.assertEqual(response.status_code, 401)

    def test_should_not_export_hymnary_to_another_user(self):
        response = self.client.get('/api/hymnary/2/export')

        self.assertEqual(response.status_code, 404)

    def test_should_not_export_hymnary_not_found(self):
        response = self.client.get('/api/hymnary/999/export')

        self.assertEqual(response.status_code, 404)
