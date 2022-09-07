from django.contrib import admin
from django.urls import include, path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_details'),
    path('books/<int:pk>/media/', views.book_media, name='book_media'),
    path('books-search/', views.book_search, name='book_search'),
    path('publisher/<int:pk>/', views.publisher_edit, name='publisher_edit'),
    path('publisher/new/', views.publisher_edit, name='publisher_create'),
    path('books/<int:book_pk>/reviews/new/ ', views.review_edit, name='review_edit'),
    path('books/<int:book_pk>/reviews/<int:review_pk>/ ', views.review_edit, name='review_edit'),
]
