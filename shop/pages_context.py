from .models import Category

def show_category_menu(context):
    categories_menu = Category.objects.filter(available=True)
    return {'categories_menu': categories_menu}