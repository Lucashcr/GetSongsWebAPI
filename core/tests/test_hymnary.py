from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient

from core.models import Hymnary


class TestHymnaryViewSet(APITestCase):
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

    def test_should_create_hymnary(self):
        hymnary_data = {
            'title': 'Test Hymnary',
        }

        response = self.client.post(
            '/api/hymnary/',
            hymnary_data,
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'Test Hymnary')
        self.assertEqual(response.data['template'], 'single-column')
        self.assertEqual(response.data['owner'], self.user.id)

    def test_should_not_create_hymnary_without_title(self):
        hymnary_data = {'title': ''}

        response = self.client.post('/api/hymnary/', hymnary_data)

        self.assertEqual(response.status_code, 400)

    def test_should_not_create_hymnary_without_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='')

        hymnary_data = {'title': 'Test Hymnary'}

        response = self.client.post('/api/hymnary/', hymnary_data)

        self.assertEqual(response.status_code, 401)

    def test_should_not_create_hymnary_to_another_user(self):
        hymnary_data = {
            'title': 'Test Hymnary',
            'owner': self.another_user.id,
        }
        response = self.client.post('/api/hymnary/', hymnary_data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['owner'], self.user.id)

    def test_shuold_get_empty_hymnaries_list(self):
        response = self.client.get('/api/hymnary/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_shuold_get_hymnaries_list(self):
        Hymnary.objects.create(title='Test Hymnary', owner=self.user)

        response = self.client.get('/api/hymnary/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Hymnary')
        self.assertEqual(response.data[0]['template'], 'single-column')
        self.assertEqual(response.data[0]['owner'], self.user.id)

    def test_should_not_get_another_users_hymnaries_list(self):
        Hymnary.objects.create(title='Test Hymnary', owner=self.another_user)

        response = self.client.get('/api/hymnary/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_should_get_hymnary(self):
        hymnary = Hymnary.objects.create(
            title='Test Hymnary',
            owner=self.user,
        )

        response = self.client.get(f'/api/hymnary/{hymnary.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Test Hymnary')
        self.assertEqual(response.data['template'], 'single-column')
        self.assertEqual(response.data['owner'], self.user.id)

    def test_should_not_get_another_users_hymnary(self):
        hymnary = Hymnary.objects.create(
            title='Test Hymnary',
            owner=self.another_user,
        )

        response = self.client.get(f'/api/hymnary/{hymnary.id}/')

        self.assertEqual(response.status_code, 404)