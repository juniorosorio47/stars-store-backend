from django.db.models import Max
from django.test import Client, TestCase

from .models import Product

# Product tests
class ProductTestCase(TestCase):

    def setUp(self):

        # Create products.
        Product.objects.create(
            name="Product 1", 
            description="Description of Product 1", 
            image="https://m.media-amazon.com/images/I/51Vy2Jb7InL.jpg",
            price=120,
            inventory=1
        )

        Product.objects.create(
            name="Product 2", 
            description="Description of Product 2", 
            image="https://m.media-amazon.com/images/I/51Vy2Jb7InL.jpg",
            price=120,
            inventory=200, 
            multiple=5
        )


    def test_decrease_inventory_valid_multiple(self):
        """Decrease inventory with valid multiple"""
        product = Product.objects.get(name="Product 2")
        inventory = product.inventory
        quantity = 50

        product.decrease_inventory(quantity)

        self.assertEqual(product.inventory, inventory - quantity)


    def test_decrease_inventory_invalid_quantity(self):
        """Decrease inventory with invalid quantity"""
        product = Product.objects.get(name="Product 1")
        quantity = 20

        result = product.decrease_inventory(quantity)

        self.assertFalse(result)


    def test_decrease_inventory_invalid_multiple(self):
        """Decrease inventory with invalid multiple"""
        product = Product.objects.get(name="Product 2")
        quantity = 3
        result = product.decrease_inventory(quantity)

        self.assertFalse(result)


    def test_increase_inventory(self):
        """Increase inventory"""
        product = Product.objects.get(name="Product 2")
        inventory = product.inventory
        quantity = 50

        product.increase_inventory(quantity)

        self.assertEqual(product.inventory, inventory + quantity)


    def test_valid_multiple(self):
        """Valid multiple"""
        product = Product.objects.get(name="Product 2")
        quantity = 20
        
        result = product.is_multiple(quantity)
        
        self.assertTrue(result)


    def test_invalid_multiple(self):
        """Invalid multiple"""
        product = Product.objects.get(name="Product 2")
        quantity = 18

        result = product.is_multiple(quantity)

        self.assertFalse(result)


    def test_has_inventory_valid(self):
        """Valid inventory quantity"""
        product = Product.objects.get(name="Product 2")
        quantity = 20

        result = product.has_inventory(quantity)

        self.assertTrue(result)


    def test_has_inventory_invalid(self):
        """Invalid inventory quantity"""
        product = Product.objects.get(name="Product 1")
        quantity = 20

        result = product.has_inventory(quantity)

        self.assertFalse(result)


    def test_index(self):
        """Products index"""
        client = Client()
        
        response = client.get('/api/products')

        self.assertEqual(response.status_code, 200)
    

    def test_create(self):
        """Product create"""
        client = Client()

        product = {
            "name":"Spaceship 2912",
            "description":"Big spaceship",
            "image":"https://m.media-amazon.com/images/I/51Vy2Jb7InL.jpg",
            "price":20000,
            "inventory": 2,
            "multiple":1
        }

        response = client.post('/api/products', product)
        
        product_id = response.data.get("data").get("id")
        
        check_product_exists = client.get(f'/api/products/{product_id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(check_product_exists.status_code, 200)


    def test_update(self):
        """Product update"""
        client = Client()
        product = Product.objects.get(name='Product 1')

        product_new_info = {
            "price":50000.00,
            "inventory": 23,
        }

        response = client.put(f'/api/products/{str(product.id)}', product_new_info, content_type='application/json')

        product_updated = client.get(f'/api/products/{product.id}').data.get('data')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(float(product_updated.get('price')), product_new_info.get('price'))
        self.assertEqual(int(product_updated.get('inventory')), product_new_info.get('inventory'))
