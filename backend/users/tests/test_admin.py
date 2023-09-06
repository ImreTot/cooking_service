from django.test import TestCase

from users.admin import UserCreationForm


class UserCreationFormTest(TestCase):

    def setUp(self):
        self.form_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }

    def test_clean_password2_with_matching_passwords(self):
        """
        User creation form pasts validation with correct data.
        """
        form = UserCreationForm(data=self.form_data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

    def test_clean_password2_with_non_matching_passwords(self):
        """
        User create form returns error
        when trying to create user with non-matching passwords.
        """
        form_data = self.form_data.copy()
        form_data['password2'] = 'differentpassword'
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_save_method_saves_user_with_correct_password(self):
        """
        User create form creates user instance with correct password.
        """
        form = UserCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(user.check_password(self.form_data['password1']))
