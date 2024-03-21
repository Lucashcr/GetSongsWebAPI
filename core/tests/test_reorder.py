from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient

from api.models import Artist, Category, Song
from core.models import Hymnary, HymnarySong


class TestReorderSongsAPIView(APITestCase):
    client_class = APIClient

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token = self.client.post(
            "/user/token/", {"username": "testuser", "password": "testpassword"}
        ).json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.another_user = User.objects.create_user(
            username="anotheruser", password="anotherpassword"
        )

        self.song1 = Song.objects.create(
            name="Test Song 1",
            slug="test-song-1",
            artist=Artist.objects.create(
                name="Test Artist 1",
                slug="test-artist-1",
            ),
            category=Category.objects.create(
                name="Test Category", slug="test-category"
            ),
            lyrics="Test Lyrics 1",
        )

        self.song2 = Song.objects.create(
            name="Test Song 2",
            slug="test-song-2",
            artist=Artist.objects.create(
                name="Test Artist 2",
                slug="test-artist-2",
            ),
            category=Category.objects.create(
                name="Test Category", slug="test-category"
            ),
            lyrics="Test Lyrics 2",
        )

        self.hymnary = Hymnary.objects.create(
            title="Test Hymnary",
            owner=self.user,
        )
        self.hymnary.songs.add(self.song1, through_defaults={"order": 1})
        self.hymnary.songs.add(self.song2, through_defaults={"order": 2})

        self.another_hymnary = Hymnary.objects.create(
            title="Test Hymnary",
            owner=self.another_user,
        )
        self.another_hymnary.songs.add(self.song1, through_defaults={"order": 1})
        self.another_hymnary.songs.add(self.song2, through_defaults={"order": 2})

    def test_should_reorder_songs(self):
        hymnarysong1 = HymnarySong.objects.get(hymnary=self.hymnary, song=self.song1)
        hymnarysong2 = HymnarySong.objects.get(hymnary=self.hymnary, song=self.song2)

        self.assertEqual(hymnarysong1.order, 1)
        self.assertEqual(hymnarysong2.order, 2)

        response = self.client.post(
            f"/api/hymnary/{self.hymnary.id}/reorder/",
            {"songs": [self.song2.id, self.song1.id]},
        )

        self.assertEqual(response.status_code, 200)

        hymnarysong1 = HymnarySong.objects.get(hymnary=self.hymnary, song=self.song1)
        hymnarysong2 = HymnarySong.objects.get(hymnary=self.hymnary, song=self.song2)

        self.assertEqual(hymnarysong1.order, 2)
        self.assertEqual(hymnarysong2.order, 1)

    def test_should_not_reorder_songs_if_hymnary_does_not_exist(self):
        response = self.client.post(
            "/api/hymnary/999/reorder/", {"songs": [self.song2.id, self.song1.id]}
        )

        self.assertEqual(response.status_code, 404)

    def test_should_not_reorder_songs_if_user_is_not_owner(self):
        response = self.client.post(
            f"/api/hymnary/{self.another_hymnary.id}/reorder/",
            {"songs": [self.song2.id, self.song1.id]},
        )

        self.assertEqual(response.status_code, 404)

    def test_should_not_reorder_songs_if_songs_is_not_provided(self):
        response = self.client.post(
            f"/api/hymnary/{self.hymnary.id}/reorder/", {"songs": []}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), "Atributo songs não enviado")
