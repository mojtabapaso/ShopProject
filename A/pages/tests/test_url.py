from django.test import TestCase
from django.urls import reverse
from pages.models import Category
from products.models import Products, Brand, Commend
from django.contrib.auth import get_user_model

User = get_user_model()


class HomeTest(TestCase):
    def test_first_url(self):
        url = ''
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='pages/index.html')

    def test_second_url(self):
        response = self.client.get(reverse('pages:category_slug', args=['slug']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='pages/index.html')


class ProductsDetailTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name='test', is_sub_category=True, slug='slug-test')
        brand = Brand.objects.create(name='test-brand')
        brand.category.set([category])
        self.product = Products.objects.create(title='title_test', price=1000, slug='slug-test-product',
                                               description='test description for product', is_active=True, quantity=1,
                                               image='test_image.jpg', brand=brand, category=category)

    def test_url(self):
        response = self.client.get(reverse('pages:product_detail', args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='pages/detail.html')


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

    def test_url(self):
        url = reverse('pages:add_reply', args=[self.product.id, self.comment.id])
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, template_name='pages/detail.html')
