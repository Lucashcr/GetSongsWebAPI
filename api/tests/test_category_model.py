from django.test import TestCase

from api.models import Category


class TestCategories(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Category 1", slug="category-1")

    def test_category_str(self):
        self.assertEqual(str(self.category), "Category 1")
