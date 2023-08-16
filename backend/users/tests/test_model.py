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
        """
        Custom model creates user instance with correct data.
        """
        fields_titles = {
            self.first_user.email: self.user_data['email'],
            self.first_user.username: self.user_data['username'],
            self.first_user.first_name: self.user_data['first_name'],
            self.first_user.last_name: self.user_data['last_name'],
            self.first_user.is_active: True,
            self.first_user.has_perm('some_permission'): True,
            self.first_user.has_module_perms('some_app_label'): True,
            self.first_user.is_staff: False,
            self.first_user.is_admin: False,
        }
        for value, expected in fields_titles.items():
            with self.subTest(value=value):
                self.assertEqual(
                    value, expected,
                    f'Field -{str(value)}- '
                    f'in user instance'
                    f'return incorrect value -{value}. '
                    f'Expected value -{expected}-.'
                )

    def test_create_superuser(self):
        """
        Custom model creates superuser instance with correct data.
        """
        user_data = self.user_data.copy()
        user_data['email']  = 'admin_test@example.com'
        user_data['username'] = 'admin_testuser'
        admin = self.User.objects.create_superuser(**user_data)
        fields_titles = {
            admin.email: user_data['email'],
            admin.username: user_data['username'],
            admin.first_name: user_data['first_name'],
            admin.last_name: user_data['last_name'],
            str(admin): user_data['email'],
            admin.is_active: True,
            admin.is_admin: True,
            admin.has_perm('some_permission'): True,
            admin.has_module_perms('some_app_label'): True,
            admin.is_staff: True,
        }
        for value, expected in fields_titles.items():
            with self.subTest(value=value):
                self.assertEqual(
                    value, expected,
                    f'Field -{str(value)}- '
                    f'in superuser instance'
                    f'return incorrect value -{value}. '
                    f'Expected value -{expected}-.'
                )

    def test_username_unique(self):
        """
        User model can't create user instance with existing username.
        """
        second_user_data = self.user_data.copy()
        second_user_data['email'] = 'another@example.com'
        with self.assertRaises(Exception):
            user2 = self.User.objects.create_user(**second_user_data)

    def test_email_unique(self):
        """
        User model can't create user instance with existing email.
        """
        second_user_data = self.user_data.copy()
        second_user_data['username'] = 'anotheruser'
        with self.assertRaises(Exception):
            user2 = self.User.objects.create_user(**second_user_data)

    def test_create_user_with_missing_email(self):
        """
        User model can't create user instance without email.
        """
        user_data = self.user_data.copy()
        user_data['email'], user_data['username'] = '', 'testuser2'
        with self.assertRaises(ValueError) as context:
            user = self.User.objects.create_user(**user_data)
        self.assertIn('Users must have an email address', str(context.exception))
