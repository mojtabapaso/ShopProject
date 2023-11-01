from django.urls import reverse, resolve

from ..views import *
from django.test import TestCase, Client


class RegisterViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone_number='09335215295', password='1234')
        self.client = Client()

    def test_view_register(self):
        url = reverse('accounts:register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(url).func.view_class, RegisterView)
        self.assertTemplateUsed(response, template_name='accounts/register.html')


class VerifyViewTest(TestCase):
    def test_verify(self):
        url = reverse('accounts:verify_code')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(url).func.view_class, VerifyCodeRegisterView)
        self.assertTemplateUsed(response, template_name='accounts/verify.html')


class LoginViewTest(TestCase):
    def test_login(self):
        url = reverse('accounts:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(url).func.view_class, LoginView)

        self.assertTemplateUsed(response, template_name='accounts/login.html')


class LogoutViewTest(TestCase):
    def test_logout(self):
        url = reverse('accounts:logout')
        response = self.client.get(url, follow=True)
        self.assertEqual(resolve(url).func.view_class, LogoutView)
        self.assertEqual(response.status_code, 200)


class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(phone_number='09335215295', password='1234')
        self.client = Client()

    def test_profile(self):
        self.client.login(phone_number='09335215295', password='1234')
        url = reverse('accounts:profile')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(url).func.view_class, ProfileView)
        self.assertTemplateUsed(response, template_name='accounts/profile.html')


class ChangeProfileViewTest(TestCase):
    def test_change_profile(self):
        url = reverse('accounts:change_profile')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(url).func.view_class, ChangeProfile)


class ChangeDateBirthViewTest(TestCase):
    def test_change_birth(self):
        url = reverse('accounts:change_birth')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(url).func.view_class, ChangeDateBirth)


class ChangePasswordViewTest(TestCase):
    def test_change_password(self):
        url = reverse('accounts:change_password')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(url).func.view_class, ChangePasswordView)


class ForgetPasswordViewTest(TestCase):
    def test_forget_password(self):
        url = reverse('accounts:forget_password')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(url).func.view_class, ForgetPasswordView)


class VerifyCodePasswordViewTest(TestCase):
    def test_verify_password(self):
        url = reverse('accounts:verify_password')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(url).func.view_class, VerifyCodePasswordView)


class CreateNewPasswordViewTest(TestCase):
    def test_create_new_password(self):
        url = reverse('accounts:create_password')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(url).func.view_class, CreateNewPasswordView)
