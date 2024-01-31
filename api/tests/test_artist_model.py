from django.test import TestCase

from api.models import Artist


class TestCategories(TestCase):
    def setUp(self):
        self.artist = Artist.objects.create(
            name='Artist 1',
            slug='artist-1'
        )

    def test_category_str(self):
        self.assertEqual(str(self.artist), 'Artist 1')
