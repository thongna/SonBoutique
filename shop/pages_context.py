from .models import Category, Link
from others.models import Contact

def show_category_menu(context):
    categories_menu = Category.objects.filter(available=True)
    return {'categories_menu': categories_menu}

def get_url(context):
    urls = Link.objects.filter(active=True)
    return {'urls': urls}

def get_contact(context):
    son_boutique_contact = Contact.objects.get(name="Son Boutique")
    return {'son_boutique_contact': son_boutique_contact}