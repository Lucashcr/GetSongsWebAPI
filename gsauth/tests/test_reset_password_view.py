import uuid
from django.test import TestCase, override_settings
from django.contrib.auth.models import User

from gsauth.models import PasswordRecoveryToken


class TestResetPasswordAPIView(TestCase):
    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def setUp(self):
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

        self.client.post(
            "/user/forgot-password/",
            {
                "email": self.email,
            },
        )

        self.token = PasswordRecoveryToken.objects.create(
            user=User.objects.get(username=self.username), is_valid=True
        )

    def test_should_not_get_reset_password_with_no_token(self):
        response = self.client.get(
            "/user/reset-password/",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"ok": False})

    def test_should_not_get_reset_password_with_invalid_token(self):
        response = self.client.get(
            "/user/reset-password/", QUERY_STRING=f"t={uuid.uuid4().hex}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"ok": False})

    def test_should_not_get_reset_password_with_expired_token(self):
        token = PasswordRecoveryToken.objects.create(
            user=User.objects.get(username=self.username), is_valid=False
        )

        response = self.client.get(
            "/user/reset-password/", QUERY_STRING=f"t={token.token}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"ok": False})

    def test_should_get_reset_password(self):
        response = self.client.get(
            "/user/reset-password/", QUERY_STRING=f"t={self.token.token}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"ok": True})

    def test_should_not_post_reset_password_without_token(self):
        response = self.client.post(
            "/user/reset-password/",
            {
                "password": uuid.uuid4().hex,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"ok": False, "messages": ["Dados inválidos"]}
        )

    def test_should_not_post_reset_password_with_invalid_token(self):
        response = self.client.post(
            "/user/reset-password/",
            {
                "token": uuid.uuid4().hex,
                "password": uuid.uuid4().hex,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"ok": False, "messages": ["Dados inválidos"]}
        )

    def test_should_not_post_reset_password_without_password(self):
        response = self.client.post(
            "/user/reset-password/",
            {
                "token": self.token.token,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"ok": False, "messages": ["Dados inválidos"]}
        )

    def test_should_post_reset_password(self):
        response = self.client.post(
            "/user/reset-password/",
            {
                "token": self.token.token,
                "password": uuid.uuid4().hex,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"ok": True, "messages": ["Senha alterada com sucesso"]}
        )
