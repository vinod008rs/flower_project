from django.core.management.base import BaseCommand

from orders.models import Product, Bundle


class Command(BaseCommand):
    help = 'Initialize the database with product and bundle data'

    def handle(self, *args, **kwargs):
        # Define the product data
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

        self.stdout.write(self.style.SUCCESS('Database initialized with product and bundle data.'))
