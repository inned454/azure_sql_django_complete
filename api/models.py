from datetime import timezone
from django.db import models

# Create your models here.


class Store(models.Model):
    # Model representing a physical store location
    store_id = models.IntegerField(unique=True)
    store_location = models.CharField(max_length=100)

    # String representation of the store
    def __str__(self):
        return f"{self.store_id} - {self.store_location}"


class Product(models.Model):
    # Model representing a product available in a store
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # String representation of the product
    def __str__(self):
        return self.name
