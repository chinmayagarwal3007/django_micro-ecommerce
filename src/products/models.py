from django.db import models
from django.conf import settings
from django.utils import timezone

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    handle = models.SlugField(unique=True)
    long_description = models.TextField(null=True)
    short_description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    og_price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    stripe_price = models.IntegerField(default=999)
    price_changed_timestamp = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)  
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.price != self.og_price:
            self.og_price = self.price
            self.stripe_price = int(self.price * 100)
            self.price_changed_timestamp = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Product: {self.name}'