from unittest.mock import MagicMock, patch
import uuid

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase


User = get_user_model()


class TestSendmailView(APITestCase):
    def setUp(self):
        User.objects.create_superuser(
            username="admin",
            password="admin123",
            email="admin@email.com",
            first_name="Admin",
            last_name="User",
        )

        self.username = "usertest"
        self.first_name = "Test"
        self.last_name = "User"
        self.email = "testuser@email.com"
        self.password = uuid.uuid4().hex

        self.client.post(
            "/user/register/",
            {
                "first_name": self.first_name,
                "last_name": self.last_name,
                "username": self.username,
                "password": self.password,
                "email": self.email,
            },
        )

        self.token = self.client.post(
            "/user/token/",
            {
                "username": self.username,
                "password": self.password,
            },
        ).json()["token"]

    @patch("services.email.EmailService.send")
    def test_should_send_email(self, send_method_mock: MagicMock):
        send_method_mock.return_value = 1

        response = self.client.post(
            "/user/sendmail/",
            {
                "name": "Test User",
                "email": self.email,
                "message": "Test message",
            },
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )

        send_method_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Email enviado com sucesso")

    @patch("services.email.EmailService.send")
    def test_should_send_email_without_name(self, send_method_mock: MagicMock):
        send_method_mock.return_value = 1

        response = self.client.post(
            "/user/sendmail/",
            {
                "email": self.email,
                "message": "Test message",
            },
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )

        send_method_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Email enviado com sucesso")

    @patch("services.email.EmailService.send")
    def test_should_send_email_without_email(self, send_method_mock: MagicMock):
        send_method_mock.return_value = 1

        response = self.client.post(
            "/user/sendmail/",
            {
                "name": "Test User",
                "message": "Test message",
            },
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )

        send_method_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Email enviado com sucesso")

    @patch("services.email.EmailService.send")
    def test_should_not_send_email_without_message(self, send_method_mock: MagicMock):
        send_method_mock.return_value = 1

        response = self.client.post(
            "/user/sendmail/",
            {
                "name": "Test User",
                "email": self.email,
            },
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )

        send_method_mock.assert_not_called()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), "Dados inválidos")
