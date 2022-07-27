from django.test import TestCase
from .models import Store

# Create your tests here.
class TestViews(TestCase):

    def test_store(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

    def test_add_products_page(self):
        response = self.client.get('/add')
        self.assertEqual(response.status_code, 301)

    # def test_edit_products_page(self):
        product = Store.objects.create(name='Test Store Product')
        response = self.client.get(f'/edit/{product.id}')
        self.assertEqual(response.status_code, 301)

    def test_can_add_product(self):
        response = self.client.post('/add', {'name': 'Test Added Product'})
        self.assertEqual(response.status_code, 301)

    def test_can_delete_product(self):
        product = Store.objects.create(name='Test Store Product')
        response = self.client.post(f'/delete/{product.id}')
        self.assertEqual(response.status_code, 301)