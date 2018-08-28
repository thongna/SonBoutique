from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('import-expense/', views.import_expense, name='import-expense'),

]