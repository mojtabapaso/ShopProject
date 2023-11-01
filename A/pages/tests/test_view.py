from django.test import TestCase
from django.urls import reverse, resolve
from products.models import Brand
from ..views import *
from django.contrib.auth import get_user_model

User = get_user_model()


class HomeTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name='test', is_sub_category=True, slug='slug-test')
        brand = Brand.objects.create(name='test-brand')
        self.product = Products.objects.create(title='title_test', price=1000, slug='slug-test-product',
                                               description='test description for product', is_active=True, quantity=1,
                                               image='test_image.jpg', brand=brand, category=category)

    def test_view_home(self):
        url = reverse('pages:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(url).func.view_class, HomeView)

    def test_second_view(self):
        url = reverse('pages:category_slug', args=[self.product.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(url).func.view_class, HomeView)

class AddCommendTest(TestCase):
    def setUp(self):
        user = User.objects.create(phone_number='09123456789', password='123456')
        category = Category.objects.create(name='test', is_sub_category=True, slug='slug-test')
        brand = Brand.objects.create(name='test-brand')
        self.product = Products.objects.create(title='title_test', price=1000, slug='slug-test-product',
                                               description='test description for product', is_active=True, quantity=1,
                                               image='test_image.jpg', brand=brand, category=category)
        self.comment = Commend.objects.create(user=user, product=self.product, is_reply=False, body='test',
                                              active=False)
    def test_view(self):
        url = reverse('pages:add_reply', args=[self.comment.id, self.product.id])
        self.assertEqual(resolve(url).func.view_class, AddCommendView)
