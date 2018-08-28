from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('all/', views.product_list, name='product_list_all'),
    path('<slug:category_slug>/', views.category, name='product_list_by_category'),
    path('collection/<int:id>/', views.product_list, name='product_list_by_collection'),
    path('collection/list/', views.collection_list, name='collection_list'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('tag/<slug:tag_slug>/', views.product_list, name='post_list_by_tag'),
    path('best-saled/<int:best_saled>/', views.product_list, name='best_saled_product'),

]