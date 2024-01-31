import uuid
from django.test import TestCase, override_settings


class TestSendmailView(TestCase):
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

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_should_send_email(self):
        response = self.client.post('/user/forgot-password/', {
            'email': self.email,
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {'ok': True, 'message': 'Email enviado com sucesso'}
        )

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_should_not_send_email_without_email(self):
        response = self.client.post('/user/forgot-password/', {
            'email': '',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {'ok': False, 'message': 'Email não pode ser vazio'}
        )

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_should_not_send_email_with_invalid_email(self):
        response = self.client.post('/user/forgot-password/', {
            'email': 'invalidemail',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {'ok': True, 'message': 'Email enviado com sucesso'}
        )
