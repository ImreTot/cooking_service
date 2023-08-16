from django.test import TestCase

from recipes.models import Tag, Ingredient, Recipe
from users.models import CustomUser

class RecipeModelsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = CustomUser.objects.create(
            email='test@example.com',
            username='testuser',
            first_name='John',
            last_name='Doe',
            password='testpassword',
        )
        cls.tag = Tag.objects.create(
            name='test tag',
            color='#000000',
            slug='test_tag')
        cls.ingredient = Ingredient.objects.create(name='test ing')
        cls.recipe = Recipe.objects.create(
            author=cls.user,
            name='test recipe',
            text='test text',
            cooking_time=1,
        )

    def test_models_have_correct_object_names(self):
        """Models create objects which return __str__ of instances."""
        fields_titles = {
            self.tag: 'test tag',
            self.ingredient: 'test ing',
            self.recipe: 'test recipe',
        }
        for value, expected in fields_titles.items():
            with self.subTest(value=value):
                self.assertEqual(
                    str(value), expected,
                    f'Instance -{value}- of models '
                    f'creates incorrect __str__ name.'
                    f'Expected value -{expected}-.'
                )