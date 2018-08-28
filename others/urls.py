from django.urls import path
from . import views

app_name = 'others'

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('review/', views.review_list, name='reviews'),
    path('review-active/', views.review_active, name='review_active'),
    path('faq/', views.faq, name='faq'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('messages/', views.message_list, name='messages'),
    path('message-readed/', views.message_readed, name='readed'),

]
