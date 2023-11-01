from ..models import User, Profile
from django.test import TestCase


class UserModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(phone_number='09335215295', password='123456')
        admin = User.objects.create_superuser(phone_number='09331111111', password='123456')

    def test_user(self):
        user = User.objects.get(id=1)
        phone_number = f'{user.phone_number}'
        password = f'{user.password}'
        self.assertFalse(password == '123456')
        self.assertEqual(phone_number, '09335215295')
        self.assertFalse(user.is_admin)
        self.assertTrue(user.is_active)

    def test_user_admin(self):
        admin = User.objects.get(id=2)
        phone_number = f'{admin.phone_number}'
        password = f'{admin.password}'
        self.assertFalse(password == '123456')
        self.assertEqual(phone_number, '09331111111')
        self.assertTrue(admin.is_admin)
        self.assertTrue(admin.is_active)

    def test_str_user(self):
        """ test __str__ """
        user = User(phone_number='09331111111')
        self.assertEqual(str(user), user.phone_number)




class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone_number='09331111111', password='123456')
        Profile.objects.update(user=self.user, date_of_berth='1379-12-28', first_name='mojtaba',
                               last_name='ataei', email='mojtabapaso@gmail.com', address='just a test address')
        self.profile = Profile.objects.get(user=self.user)

    def test_profile(self):
        """ test data in profile """
        profile = Profile.objects.get(id=1)
        self.assertEqual(profile.first_name, self.profile.first_name)
        self.assertEqual(profile.last_name, self.profile.last_name)
        self.assertEqual(profile.date_of_berth, self.profile.date_of_berth)
        self.assertEqual(profile.email, self.profile.email)
        self.assertEqual(profile.user.phone_number, self.profile.user.phone_number)
        self.assertEqual(profile.address, self.profile.address)

    def test_one_profile(self):
        """ test for every user just one profile no two or more """
        profile = Profile.objects.get(id=1)
        self.assertTrue(len(profile.user.phone_number), 1)
        self.assertTrue(len(self.profile.user.phone_number), 1)

    def test_str_profile(self):
        """ __str__"""
        profile = Profile.objects.get(id=1)
        self.assertEqual(str(profile.user), str(self.user.phone_number))
