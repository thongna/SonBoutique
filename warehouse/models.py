from django.db import models
from shop.models import Product
from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User

# Create your models here.
class StockIn(models.Model):
    product = models.ForeignKey(Product,related_name='stock_in', on_delete=models.CASCADE)
    origin_price = models.DecimalField(max_digits=10, decimal_places=0)
    sale_price = models.DecimalField(max_digits=10, decimal_places=0)
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    create_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('-created',)


@receiver(post_save, sender=StockIn)
def update_quantity_of_product(sender, instance, created, *args, **kwargs):
    if created:
        product = Product.objects.get(id=instance.product.id)
        product.price = instance.sale_price
        product.stock += instance.quantity
        product.save()