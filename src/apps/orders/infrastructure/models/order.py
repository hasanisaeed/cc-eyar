from django.db import models
from django.conf import settings


class Order(models.Model):
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    total_price = models.PositiveBigIntegerField()
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
