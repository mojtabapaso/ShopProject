from django.test import TestCase
from ..forms import *


class UserCreationFormTest(TestCase):
    def test_form(self):
        form_data = {'password1': '123456MMm', 'password2': '123456MMm', 'phone_number': '09335215295'}
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())


class UserChangeFormTest(TestCase):
    def test_form_change(self):
        form_data = {'phone_number': '09335215295', 'password': '123456', 'is_active': True, 'is_admin': False}
        form = UserChangeForm(data=form_data)
        self.assertTrue(form.is_valid())


class UserRegisterFormTest(TestCase):
    def test_form(self):
        form_data = {'phone_number': '09335215295', 'password_1': '123456MMmm', 'password_2': '123456MMmm'}
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())


class VerifyCodeFormTest(TestCase):
    def test_from(self):
        form_data = {'code': '12345'}
        form = VerifyCodeForm(data=form_data)
        self.assertTrue(form.is_valid())


class UserLoginFormTest(TestCase):
    def test_from(self):
        form_data = {'phone_number': '09335215295', 'password': '123456MMmm'}
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())


class ChangePasswordFormTest(TestCase):
    def test_from(self):
        form_data = {'password_1': '123456MMmm', 'password_2': '123456MMmm'}
        form = ChangePasswordForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_from_extra(self):
        from_data = {'password_1': '12345', 'password_2': '12345'}
        form = ChangePasswordForm(data=from_data)
        self.assertFalse(form.is_valid())


class DateBirthFormTest(TestCase):
    def test_from(self):
        form_data = {'year': '1379', 'mount': '2', 'day': '12'}
        form = DateBirthForm(data=form_data)
        self.assertTrue(form.is_valid())


class ProfileFormTest(TestCase):
    def test_from(self):
        form_data = {'first_name': 'mojtaba', 'last_name': 'ataei', 'email': 'mojtaba@gamil.com'}
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())


class NumberPhoneForgetPasswordTest(TestCase):
    def test_form(self):
        form_data = {'number_phone': '09123456789'}
        form = NumberPhoneForgetPassword(data=form_data)
        self.assertTrue(form.is_valid())
