import uuid
from django.test import TestCase, override_settings


class TestChangePasswordAPIView(TestCase):
    def setUp(self):
        self.username = 'usertest'
        self.first_name = 'Test'
        self.last_name = 'User'
        self.email = 'testuser@email.com'
        self.password = uuid.uuid4().hex

        self.client.post('/user/register/', {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'password': self.password,
            'email': self.email,
        })

        self.token = self.client.post('/user/token/', {
            'username': self.username,
            'password': self.password,
        }).json()['access']

    def test_should_change_password(self):
        response = self.client.post('/user/change-password/', {
            'old_password': self.password,
            'new_password': uuid.uuid4().hex,
        }, HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {'ok': True, 'messages': ['Senha alterada com sucesso']}
        )

    def test_should_not_change_password_if_old_password_is_wrong(self):
        response = self.client.post('/user/change-password/', {
            'old_password': uuid.uuid4().hex,
            'new_password': uuid.uuid4().hex,
        }, HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {'ok': False, 'messages': ['Senha atual incorreta']}
        )

    def test_should_not_change_password_without_old_password(self):
        response = self.client.post('/user/change-password/', {
            'new_password': uuid.uuid4().hex,
        }, HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {'ok': False, 'messages': ['Dados inválidos']}
        )

    def test_should_not_change_password_without_new_password(self):
        response = self.client.post('/user/change-password/', {
            'old_password': self.password,
        }, HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {'ok': False, 'messages': ['Dados inválidos']}
        )
