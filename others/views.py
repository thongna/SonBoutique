from django.shortcuts import render
from .models import *

# Create your views here.
def contact(request):
    son_boutique_contact = Contact.objects.get(name="Son Boutique")
    return render(request, 'others/other/contact.html',
                  {'son_boutique_contact': son_boutique_contact})