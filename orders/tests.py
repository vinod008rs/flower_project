# tests.py
from django.test import TestCase, Client
from django.urls import reverse
from .models import Product, Order, OrderItem, Bundle
from decimal import Decimal


class OrderViewTests(TestCase):
    def setUp(self):
        # Setup a client to use in tests
        self.client = Client()
        # Create product and bundle data
        products = [
            {'name': 'Roses', 'code': 'R12', 'bundles': [(5, 6.99), (10, 12.99)]},
            {'name': 'Lilies', 'code': 'L09', 'bundles': [(3, 9.95), (6, 16.95), (9, 24.95)]},
            {'name': 'Tulips', 'code': 'T58', 'bundles': [(3, 5.95), (5, 9.95), (9, 16.99)]},
        ]

        # Create each product and its bundles
        for product_data in products:
            product, created = Product.objects.get_or_create(name=product_data['name'], code=product_data['code'])
            for quantity, price in product_data['bundles']:
                Bundle.objects.get_or_create(product=product, quantity=quantity, price=price)

    # ... Create bundles for this product if needed ...

    def test_valid_order_submission(self):
        # Test submitting a valid order
        response = self.client.post(reverse('place_order'), {
            'customer_name': 'Test Customer',
            'customer_phone': '1234567890',
            'customer_address': '123 Test St',
            'customer_email': 'test@example.com',
            'order_data': '10 R12'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Order.objects.exists())
        self.assertTrue(OrderItem.objects.exists())

    def test_invalid_order_submission(self):
        # Test submitting an invalid order
        response = self.client.post(reverse('place_order'), {
            'customer_name': 'Test Customer',
            'customer_phone': '1234567890',
            'customer_address': '123 Test St',
            'customer_email': 'invalid-email',
            'order_data': '10 R12'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Order.objects.exists())
        self.assertFormError(response, 'form', 'customer_email', 'Enter a valid email address.')

    def test_form_display_on_get_request(self):
        # Test that a GET request returns the empty order form
        response = self.client.get(reverse('place_order'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_form.html')
        self.assertIn('form', response.context)
        self.assertIn('products_with_bundles', response.context)

    def test_redirect_after_successful_order(self):
        # Assume after a successful order, you redirect to a 'thank_you' page.
        response = self.client.post( reverse('place_order'),{
            'customer_name': 'Test Customer',
            'customer_phone': '1234567890',
            'customer_address': '123 Test St',
            'customer_email': 'test@example.com',
            'order_data': '10 R12'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_order_summary_context_data(self):
        # Make sure order summary context data is correct after a successful submission
        response = self.client.post(reverse('place_order'), {
            'customer_name': 'Test Customer',
            'customer_phone': '1234567890',
            'customer_address': '123 Test St',
            'customer_email': 'test@example.com',
            'order_data': '10 R12'
        })
        self.assertIn('summary', response.context)

    def test_product_does_not_exist(self):
        # Test submission with a non-existent product code
        response = self.client.post(reverse('place_order'), {
            'customer_name': 'Test Customer',
            'customer_phone': '1234567890',
            'customer_address': '123 Test St',
            'customer_email': 'test@example.com',
            'order_data': '10 XYZ'  # XYZ is a non-existent product code
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Order.objects.exists())
        self.assertFormError(response, 'form', 'order_data', 'Invalid product codes: XYZ')

    def test_order_with_multiple_items(self):
        # Test an order with multiple products
        # Assuming 'order_data' can handle a list of product codes and quantities
        response = self.client.post(reverse('place_order'), {
            'customer_name': 'Test Customer',
            'customer_phone': '1234567890',
            'customer_address': '123 Test St',
            'customer_email': 'test@example.com',
            'order_data': '10 R12 \n 15 L09'  # ABC is another valid product code
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(OrderItem.objects.count(), 2)

    def test_empty_order(self):
        # Test submitting an empty order
        response = self.client.post(reverse('place_order'), {
            'customer_name': 'Test Customer',
            'customer_phone': '1234567890',
            'customer_address': '123 Test St',
            'customer_email': 'test@example.com',
            'order_data': ''  # Empty order data
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Order.objects.exists())
        self.assertFormError(response, 'form', 'order_data', 'This field is required.')

    def test_order_summary_calculation(self):
        # Test the order summary calculation
        # This would test the `calculate_order_summary` function indirectly via the view
        # Ensure this function is mocked if it calls external services or has side effects
        response = self.client.post(reverse('place_order'), {
            'customer_name': 'Test Customer',
            'customer_phone': '1234567890',
            'customer_address': '123 Test St',
            'customer_email': 'test@example.com',
            'order_data': '10 L09'
        })
        self.assertIn('summary', response.context)
        # Check if the summary contains the correct calculation
        summary = response.context['summary']
        self.assertEqual(round(Decimal(summary[0]['total_price']), 2), Decimal('34.9'))

    def test_form_errors_displayed(self):
        # Test that form errors are displayed to the user
        response = self.client.post(reverse('place_order'), {
            'customer_name': '',
            'customer_phone': '',
            'customer_address': '',
            'customer_email': '',
            'order_data': '10 L09'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'customer_name', 'This field is required.')
        self.assertFormError(response, 'form', 'customer_phone', 'This field is required.')
        self.assertFormError(response, 'form', 'customer_address', 'This field is required.')
        self.assertFormError(response, 'form', 'customer_email', 'This field is required.')
