from ..models import Category
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class TestCategory(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='test', is_sub_category=False, slug='slug-category')

    def test_category(self):
        category = Category.objects.get(id=1)
        self.assertEqual(category.name, self.category.name)
        self.assertFalse(category.is_sub_category)
        self.assertEqual(category.is_sub_category, self.category.is_sub_category)
        self.assertEqual(category.slug, self.category.slug)
