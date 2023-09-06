from django.test import TestCase

from api.serializers import TagSerializer
from recipes.models import Tag


class TagSerializerTest(TestCase):

    def setUp(self):
        self.tag_data = {'name': 'Test Tag'}
        self.tag = Tag.objects.create(**self.tag_data)
        self.serializer = TagSerializer(instance=self.tag)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'name', 'color', 'slug'})
