from django.test import TestCase
from django.core.exceptions import ValidationError
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
        form = UserCreationForm(data=self.form_data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

    def test_clean_password2_with_non_matching_passwords(self):
        form_data = self.form_data.copy()
        form_data['password2'] = 'differentpassword'
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_save_method_saves_user_with_correct_password(self):
        form = UserCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(user.check_password(self.form_data['password1']))
