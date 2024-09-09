from django.urls import path
from .views import BookListView, BookDetailView
from .models import Book

app_name = 'books'

urlpatterns = [
   path('list/', BookListView.as_view(), name='list'),
   # <pk> ...primary key
   path('list/<pk>', BookDetailView.as_view(), name='detail')
]