from django.test import SimpleTestCase


class RegisterUrlTest(SimpleTestCase):

    def test_register(self):
        url = '/accounts/register/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='accounts/register.html')


class VerifyUrlTest(SimpleTestCase):
    def test_verify(self):
        url = '/accounts/verify/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='accounts/verify.html')


class LoginUrlTest(SimpleTestCase):
    def test_login(self):
        url = '/accounts/login/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='accounts/login.html')


class LogoutUrlTest(SimpleTestCase):
    def test_logout(self):
        url = '/accounts/logout/'
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)


class ProfileUrlTest(SimpleTestCase):
    def test_profile(self):
        url = '/accounts/profile/'
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)


class ChangeProfileUrlTest(SimpleTestCase):
    def test_change_profile(self):
        url = '/accounts/change/profile/'
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)


class ChangeDateBirthUrlTest(SimpleTestCase):
    def test_change_birth(self):
        url = '/accounts/change/date-of-birth/'
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)


class ChangePasswordUrlTest(SimpleTestCase):
    def test_change_password(self):
        url = '/accounts/change/password/'
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)


class ForgetPasswordUrl(SimpleTestCase):
    def test_forget_password(self):
        url = '/accounts/forget/password/'
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)


class VerifyPassword(SimpleTestCase):
    def test_verify_password(self):
        url = '/accounts/verify/password/'
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)


class CreatePassword(SimpleTestCase):
    def test_create_password(self):
        url = '/accounts/create/password/'
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
