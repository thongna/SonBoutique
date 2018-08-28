from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'statisticadmin'

urlpatterns = [
    path('dashboard/', views.home, name='home'),
    path('order/', views.order, name='order'),
    path('order/day/<str:day>/', views.order, name='order_on_day'),
    path('order/month/<str:month>/', views.order, name='order_in_month'),
    path('order/paid/<int:paid>/', views.order, name='paid'),
    path('order-paid/', views.order_paid, name='order_paid'),
    path('stock/', views.stock_list, name='stock_list'),
    path('revenue/', views.revenue, name='revenue'),
    path('expenses/', views.expenses, name='expenses'),
    path('expense-list/', views.expense_list, name='expense-list'),
    path('expense-list/m=<str:month>/', views.expense_list, name='expenses_in_month'),
    path('profit/', views.profit, name='profit'),
]