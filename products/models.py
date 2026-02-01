from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.price} - {self.stock}"
