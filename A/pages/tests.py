
from django.urls import reverse, resolve
from .views import HomeView
from django.test import TestCase

class HomePageTest(TestCase):
    def setUp(self):
        url = reverse('pages:home')
        self.response = self.client.get(url)

    def test_homepage_status(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_url_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'pages/index.html')

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, 'دوربین کانن سری 6')

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'hello im not here , im just test')

    def test_homepage_resolves_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__, HomeView.as_view().__name__)
