from django.urls import path
from .views import sales_view

app_name = 'sales'

urlpatterns = [
   path('', sales_view),
]