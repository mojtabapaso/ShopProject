from ..models import Brand, Products, Commend
from pages.models import Category
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class BrandModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='test', is_sub_category=True, slug='slug-test')
        self.brand = Brand.objects.create(name='brand_test', slug='slug-test-brand')
        self.brand.category.set([self.category])

    def test_brand(self):
        brand = Brand.objects.get(id=1)
        self.assertEqual(brand.name, self.brand.name)
        self.assertEqual(brand.category, self.brand.category)
        self.assertEqual(brand.slug, self.brand.slug)


class ProductModelTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name='test', is_sub_category=True, slug='slug-test')
        brand = Brand.objects.create(name='test-brand')
        brand.category.set([category])
        self.product = Products.objects.create(title='title_test', price=1000, slug='slug-test-product',
                                               description='test description for product', is_active=True, quantity=1,
                                               image='test_image.jpg', brand=brand, category=category)

    def test_product(self):
        product = Products.objects.get(id=1)
        self.assertEqual(product.title, self.product.title)
        self.assertEqual(product.price, self.product.price)
        self.assertEqual(product.slug, self.product.slug)
        self.assertEqual(product.is_active, self.product.is_active)
        self.assertEqual(product.quantity, self.product.quantity)
        self.assertEqual(product.category, self.product.category)
        self.assertEqual(product.description, self.product.description)


class CommendTest(TestCase):
    def setUp(self):
        user = User.objects.create(phone_number='09123456789', password='123456')
        category = Category.objects.create(name='test', is_sub_category=True, slug='slug-test')
        brand = Brand.objects.create(name='test-brand')
        product = Products.objects.create(title='title_test', price=1000, slug='slug-test-product',
                                          description='test description for product', is_active=True, quantity=1,
                                          image='test_image.jpg', brand=brand, category=category)

        self.comment = Commend.objects.create(user=user, product=product, is_reply=False, body='test', active=False)

    def test_comment(self):
        comment = Commend.objects.get(id=1)
        self.assertEqual(comment.user, self.comment.user)
        self.assertEqual(comment.product, self.comment.product)
        self.assertEqual(comment.is_reply, self.comment.is_reply)
        self.assertFalse(comment.is_reply)
        self.assertEqual(comment.body, self.comment.body)
        self.assertFalse(comment.active)
        self.assertEqual(comment.active, self.comment.active)
