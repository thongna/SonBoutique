from django.urls import path
from . import views

app_name = 'others'

urlpatterns = [
    path('contact/', views.contact, name='contact'),
]