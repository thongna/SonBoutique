from .models import Category, Link

def show_category_menu(context):
    categories_menu = Category.objects.filter(available=True)
    return {'categories_menu': categories_menu}

def get_url(context):
    urls = Link.objects.filter(active=True)
    return {'urls': urls}