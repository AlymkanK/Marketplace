from django.db import models
from django.contrib.auth import get_user_model
from products_app.models import Product

class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]

    user = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, related_name='order')
    payment_method = models.CharField(max_length=255)
    order_number = models.CharField(max_length=255, unique=True)
    order_note = models.CharField(max_length=255, blank=True)
    shipping_price = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, default=0)
    total_price = models.DecimalField(
        max_digits=7, decimal_places=2, default=0)
    status = models.CharField(
        max_length=50, choices=PAYMENT_STATUS_CHOICES,
        default=PAYMENT_STATUS_PENDING)
    is_paid = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

    # additional fields
    paid_at = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    delivered_at = models.DateTimeField(
        auto_now_add=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_number

class OrderItem(models.Model):
    order = models.ForeignKey(
        'Order', on_delete=models.CASCADE, related_name='order_item')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    # additional fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order}-{self.product}"