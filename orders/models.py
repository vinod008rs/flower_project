import uuid
from django.db import models


class Product(models.Model):
    id = models.UUIDField(primary_key=True, null=False, db_index=True, unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Bundle(models.Model):
    id = models.UUIDField(primary_key=True, null=False, db_index=True, unique=True, editable=False, default=uuid.uuid4)
    product = models.ForeignKey(Product, related_name='bundles', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} @ ${self.price}'


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_date = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    customer_address = models.TextField()
    customer_email = models.EmailField()

    def __str__(self):
        return f'Order {self.id}'


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, null=False, db_index=True, unique=True, editable=False, default=uuid.uuid4)
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'
