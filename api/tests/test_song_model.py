from django.test import TestCase

from api.models import Artist, Category, Song


class SongModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Entrada", slug="entrada")

        self.artist = Artist.objects.create(
            name="Davidson Silva", slug="davidson-silva"
        )

        self.song = Song(
            name="Queremos Te ver",
            slug="queremos-te-ver",
            category=self.category,
            artist=self.artist,
            preview_url="https://www.youtube.com/watch?v=EKPQyjMpwuk",
            lyrics_url="https://www.letras.mus.br/davidson-silva/1943505/",
        )

    def test_str(self):
        self.assertEqual(str(self.song), "Queremos Te ver - Davidson Silva")

    def test_get_lyrics(self):
        lyrics = self.song.get_lyrics()
        self.assertIsNotNone(lyrics)
        self.assertIn("queremos te ver", lyrics.lower())

    def test_save_song(self):
        self.assertEqual(self.song.lyrics, "")
        self.song.save()
        self.assertNotEqual(self.song.lyrics, "")
        self.assertIn("queremos te ver", self.song.lyrics.lower())
