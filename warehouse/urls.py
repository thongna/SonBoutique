from django.urls import path
from . import views

app_name='warehouse'

urlpatterns = [
    path('import/', views.Import, name='import'),
    path('multi-import/', views.load_excel, name='load_excel'),
    path('importing-history/', views.import_list, name='importing-history'),
    path('import-excel/', views.import_by_excel, name='import_by_excel'),

]