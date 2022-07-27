from django.test import TestCase
from .forms import ProductForm

# Create your tests here.

class TestItemForm(TestCase):

    def test_item_name_is_required(self):
        form = ProductForm({'name': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors.keys())
        self.assertEqual(form.errors['name'][0], 'This field is required.')

    def test_has_sizes_is_not_required(self):
        form = ProductForm({'name': 'has_sizes'})
        self.assertFalse(form.is_valid())
