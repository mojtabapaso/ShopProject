from django.test import TestCase
from django.contrib.auth import get_user_model
from pages.models import Category
from products.models import Brand, Products
from ..models import Cart, Order, Coupon

User = get_user_model()


class CartTest(TestCase):
    def setUp(self):
        user = User.objects.create(phone_number='09123456789', password='123456')
        category = Category.objects.create(name='test', is_sub_category=True, slug='slug-test')
        brand = Brand.objects.create(name='test-brand')
        product = Products.objects.create(title='title_test', price=1000, slug='slug-test-product',
                                          description='test description for product', is_active=True, quantity=1,
                                          image='test_image.jpg', brand=brand, category=category)

        self.cart = Cart.objects.create(user=user, ordered=False, item=product, quantity=5)

    def test_value_in_mode(self):
        cart = Cart.objects.get(id=1)
        self.assertEqual(cart.user, self.cart.user)
        self.assertFalse(cart.ordered)
        self.assertEqual(cart.ordered, self.cart.ordered)
        self.assertEqual(cart.item, self.cart.item)
        self.assertEqual(cart.quantity, self.cart.quantity)

    def test_method_model(self):
        cart = Cart.objects.get(id=1)
        self.assertEqual(str(cart), f"{self.cart.quantity}تا{self.cart.item.title}")
        self.assertEqual(cart.price_item(), (self.cart.item.price * self.cart.quantity))
        self.assertEqual(5000, (self.cart.item.price * self.cart.quantity))


class OrderTest(TestCase):
    def setUp(self):
        user = User.objects.create(phone_number='09123456789', password='123456')
        category = Category.objects.create(name='test', is_sub_category=True, slug='slug-test')
        brand = Brand.objects.create(name='test-brand')
        product = Products.objects.create(title='title_test', price=1000, slug='slug-test-product',
                                          description='test description for product', is_active=True, quantity=1,
                                          image='test_image.jpg', brand=brand, category=category)
        cart = Cart.objects.create(user=user, ordered=False, item=product, quantity=5)
        self.order = Order.objects.create(user=user, address='test address', ordered=False)
        self.order.items.set([cart])

    def test_value_in_model(self):
        order = Order.objects.get(id=1)
        self.assertEqual(order.user, self.order.user)
        self.assertEqual(order.items, self.order.items)
        self.assertEqual(order.start_date, self.order.start_date)
        self.assertFalse(order.ordered)
        self.assertEqual(order.ordered, self.order.ordered)

    def test_total_value_order(self):
        order = Order.objects.get(id=1)
        item = order.items.all()
        var = 0
        for i in item:
            var += i.item.price * i.quantity
        self.assertEqual(self.order.total(), var)

    def test_str(self):
        order = Order.objects.get(id=1)
        self.assertEqual(str(order), f"{self.order.user.phone_number}")


class CouponTest(TestCase):
    def setUp(self):
        user = User.objects.create(phone_number='09123456789', password='123456')
        self.coupon = Coupon.objects.create(user=user, amount=500, min_order=1000)

    def test_value_in_model(self):
        coupon = Coupon.objects.get(id=1)
        self.assertEqual(self.coupon.user, coupon.user)
        self.assertIsNotNone(coupon.code)
        self.assertNotEqual(self.coupon.code, coupon.code)
        self.assertEqual(self.coupon.amount, coupon.amount)
        self.assertEqual(self.coupon.min_order, coupon.min_order)
        self.assertEqual(self.coupon.create, coupon.create)

    def test_str(self):
        coupon = Coupon.objects.get(id=1)
        self.assertEqual(str(coupon), coupon.code)
