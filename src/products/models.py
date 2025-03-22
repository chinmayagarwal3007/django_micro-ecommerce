from django.db import models # type: ignore
from django.conf import settings # type: ignore
from django.core.files.storage import FileSystemStorage # type: ignore
from django.utils import timezone # type: ignore

PROTECTED_MEDIA_ROOT = settings.PROTECTED_MEDIA_ROOT
protected_storage = FileSystemStorage(location=str(PROTECTED_MEDIA_ROOT))

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
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

def handle_product_attachment(instance, filename):
    return f'products/{instance.product.handle}/attachments/{filename}'
    
class ProductAttachment(models.Model):
    product = models.ForeignKey(Product, related_name="attachments", on_delete=models.CASCADE)
    file = models.FileField(upload_to=handle_product_attachment, storage=protected_storage)
    is_free = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)  
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Attachment for {self.product.name}"