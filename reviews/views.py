from django.db.models import Avg
from django.shortcuts import render, get_object_or_404

from .models import Book, Review
from .utils import average_rating


def book_list(request):
    books = Book.objects.all()
    book_list = []
    for book in books:
        reviews = book.review_set.all()
        if reviews:
            book_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            book_rating = 0
            number_of_reviews = 0
        book_list.append({
            'book': book,
            'book_rating': book_rating,
            'number_of_reviews': number_of_reviews
        })
    context = {
        'book_list': book_list
    }

    return render(request, 'reviews/books_list.html', context)


def book_detail(request, pk):
    selected_book = get_object_or_404(Book, pk=pk)
    reviews = selected_book.review_set.all()
    rating = selected_book.review_set.all().aggregate(Avg('rating'))
    context = {'selected_book': selected_book,
               'rating': rating.get('rating__avg'),
               'reviews': reviews}
    return render(request, 'reviews/book_detail.html', context)
