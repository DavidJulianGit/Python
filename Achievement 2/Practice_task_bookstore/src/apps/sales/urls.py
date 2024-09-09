from django.urls import path
from .views import sales_view

app_name = 'sales'

urlpatterns = [
   # Maps the root URL of the sales app to the sales_view function and gives this URL pattern the name 'home'.
   path('', sales_view, name='home')
]