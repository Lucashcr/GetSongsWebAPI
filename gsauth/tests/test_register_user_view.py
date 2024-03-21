import uuid
from django.test import TestCase


class TestRegisterUserView(TestCase):
    def setUp(self):
        self.password = uuid.uuid4().hex

    def test_should_register_and_login(self):
        response = self.client.post(
            "/user/register/",
            {
                "first_name": "Test",
                "last_name": "User",
                "username": "testuser",
                "password": self.password,
                "email": "teste@email.com",
            },
        )
        self.assertEqual(response.status_code, 201)

        token = self.client.post(
            "/user/token/",
            {
                "username": "testuser",
                "password": self.password,
            },
        ).json()["access"]

        response = self.client.get("/user/me/", HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "first_name": "Test",
                "last_name": "User",
                "username": "testuser",
                "full_name": "Test User",
                "email": "teste@email.com",
            },
        )

    def test_should_not_register_with_duplicated_username(self):
        self.client.post(
            "/user/register/",
            {
                "first_name": "Test1",
                "last_name": "User1",
                "username": "testuser",
                "password": self.password,
                "email": "test1@email.com",
            },
        )
        response = self.client.post(
            "/user/register/",
            {
                "first_name": "Test2",
                "last_name": "User2",
                "username": "testuser",
                "password": "test1password",
                "email": "test2@email.com",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_should_not_register_with_duplicated_email(self):
        self.client.post(
            "/user/register/",
            {
                "first_name": "Test1",
                "last_name": "User1",
                "username": "testuser1",
                "password": self.password,
                "email": "test@email.com",
            },
        )
        response = self.client.post(
            "/user/register/",
            {
                "first_name": "Test2",
                "last_name": "User2",
                "username": "testuser2",
                "password": self.password,
                "email": "test@email.com",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_should_not_register_with_invalid_email(self):
        response = self.client.post(
            "/user/register/",
            {
                "first_name": "Test",
                "last_name": "User",
                "username": "testuser",
                "password": self.password,
                "email": "invalidemail",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_should_not_register_with_too_short_password(self):
        response = self.client.post(
            "/user/register/",
            {
                "first_name": "Test",
                "last_name": "User",
                "username": "testuser",
                "password": "12345",
                "email": "test@email.com",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_should_not_register_with_only_letter_password(self):
        response = self.client.post(
            "/user/register/",
            {
                "first_name": "Test",
                "last_name": "User",
                "username": "testuser",
                "password": "password",
                "email": "test@email.com",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_should_not_register_with_only_number_password(self):
        response = self.client.post(
            "/user/register/",
            {
                "first_name": "Test",
                "last_name": "User",
                "username": "testuser",
                "password": "123456",
                "email": "test@email.com",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_should_not_register_with_containing_username_password(self):
        response = self.client.post(
            "/user/register/",
            {
                "first_name": "Test",
                "last_name": "User",
                "username": "testuser",
                "password": "testuser",
                "email": "test@email.com",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_should_not_login_with_wrong_username(self):
        response = self.client.post(
            "/user/register/",
            {
                "first_name": "Test",
                "last_name": "User",
                "username": "testuser",
                "password": "test@email.com",
            },
        )

        response = self.client.post(
            "/user/token/",
            {
                "username": "wronguser",
                "password": self.password,
            },
        )

        self.assertEqual(response.status_code, 401)

    def test_should_not_login_with_wrong_password(self):
        response = self.client.post(
            "/user/register/",
            {
                "first_name": "Test",
                "last_name": "User",
                "username": "testuser",
                "password": self.password,
            },
        )

        response = self.client.post(
            "/user/token/",
            {
                "username": "testuser",
                "password": "wrongpassword",
            },
        )

        self.assertEqual(response.status_code, 401)
