from django.test import TestCase
from django.contrib.auth import get_user_model


class CustomUserModelTest(TestCase):

    def setUp(self):
        self.User = get_user_model()
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'testpassword',
        }
        self.first_user = self.User.objects.create(**self.user_data)

    def test_create_user(self):
        self.assertEqual(self.first_user.email, self.user_data['email'])
        self.assertEqual(self.first_user.username, self.user_data['username'])
        self.assertEqual(self.first_user.first_name, self.user_data['first_name'])
        self.assertEqual(self.first_user.last_name, self.user_data['last_name'])
        self.assertTrue(self.first_user.is_active)
        self.assertFalse(self.first_user.is_admin)
        self.assertTrue(self.first_user.has_perm)
        self.assertTrue(self.first_user.has_module_perms)
        self.assertFalse(self.first_user.is_staff)

    def test_create_superuser(self):
        user_data = self.user_data.copy()
        user_data['email']  = 'admin_test@example.com'
        user_data['username'] = 'admin_testuser'
        admin = self.User.objects.create_superuser(**user_data)
        self.assertEqual(admin.email, user_data['email'])
        self.assertEqual(admin.username, user_data['username'])
        self.assertEqual(admin.first_name, user_data['first_name'])
        self.assertEqual(admin.last_name, user_data['last_name'])
        self.assertEqual(str(admin), user_data['email'])
        self.assertTrue(admin.is_active)
        self.assertTrue(admin.is_admin)
        self.assertTrue(admin.has_perm)
        self.assertTrue(admin.has_module_perms)
        self.assertTrue(admin.is_staff)

    def test_username_unique(self):
        second_user_data = self.user_data.copy()
        second_user_data['email'] = 'another@example.com'
        with self.assertRaises(Exception):
            user2 = self.User.objects.create_user(**second_user_data)

    def test_email_unique(self):
        second_user_data = self.user_data.copy()
        second_user_data['username'] = 'anotheruser'
        with self.assertRaises(Exception):
            user2 = self.User.objects.create_user(**second_user_data)

    def test_create_user_with_missing_email(self):
        user_data = self.user_data.copy()
        user_data['email'], user_data['username'] = '', 'testuser2'
        with self.assertRaises(ValueError) as context:
            user = self.User.objects.create_user(**user_data)
        self.assertIn('Users must have an email address', str(context.exception))
