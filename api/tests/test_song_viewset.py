from django.test import TestCase

from api.models import Artist, Category, Song


class TestSongViewSet(TestCase):
    def setUp(self):
        category = Category.objects.create(
            id=1, name="Test Category", slug="test-category"
        )
        artist = Artist.objects.create(
            id=1,
            name="Test Artist 1",
            slug="test-artist-1",
        )
        Song.objects.create(
            id=1,
            name="Test Song 1",
            slug="test-song-1",
            artist=artist,
            category=category,
            lyrics="Test Lyrics 1",
        )

    def test_get_songs(self):
        response = self.client.get("/api/song/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test Song 1")
        self.assertEqual(response.data[0]["slug"], "test-song-1")

    def test_get_song(self):
        response = self.client.get("/api/song/1/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Test Song 1")
        self.assertEqual(response.data["slug"], "test-song-1")

    def test_get_song_not_found(self):
        response = self.client.get("/api/song/999/")

        self.assertEqual(response.status_code, 404)

    def test_get_songs_by_artist(self):
        response = self.client.get("/api/song/?artist_id=1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test Song 1")
        self.assertEqual(response.data[0]["slug"], "test-song-1")

    def test_get_songs_by_category(self):
        response = self.client.get("/api/song/?category_id=1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test Song 1")
        self.assertEqual(response.data[0]["slug"], "test-song-1")

    def test_get_songs_by_artist_and_category(self):
        response = self.client.get("/api/song/?artist_id=1&category_id=1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test Song 1")
        self.assertEqual(response.data[0]["slug"], "test-song-1")
