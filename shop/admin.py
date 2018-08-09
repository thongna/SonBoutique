from django.contrib import admin
from .models import Category, Product, ProductImage, Comment

# Register your models here.
class ProductImageInline(admin.TabularInline):
    model = ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'parent_id', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)} #set automatically value of slug using the value of name

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_code', 'name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'product', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'body']
    list_editable = ['active']