import uuid
from django.test import TestCase


class TestGetCurrentUserView(TestCase):
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

        self.token = self.client.post(
            "/user/token/",
            {
                "username": self.username,
                "password": self.password,
            },
        ).json()["access"]

    def test_should_get_current_user(self):
        response = self.client.get(
            "/user/me/", HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "first_name": self.first_name,
                "last_name": self.last_name,
                "username": self.username,
                "full_name": f"{self.first_name} {self.last_name}",
                "email": self.email,
            },
        )
