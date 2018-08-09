from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=1, auto_created=1)
    parent_id = models.IntegerField()
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='categories/%Y/%m/%d', blank=True)
    available = models.BooleanField(default=1)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

class Color(models.Model):
    id = models.AutoField(primary_key=1, auto_created=1, unique=1)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Size(models.Model):
    id = models.AutoField(primary_key=1, auto_created=1, unique=1)
    name = models.CharField(max_length=5)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    product_code = models.CharField(max_length=50, unique=1)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    class Meta:
        ordering = ('-updated',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

class ProductImage(models.Model):
    id = models.AutoField(primary_key=1, auto_created=1, unique=1)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

class Comment(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='comments')
    name = models.CharField(max_length=80)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.product)