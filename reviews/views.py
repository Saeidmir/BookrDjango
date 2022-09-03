from django.db.models import Avg, Q
from django.shortcuts import render, get_object_or_404, redirect

from .forms import SearchFrom, PublisherForm, ReviewForm
from .models import Book, Review, Contributor, Publisher
from .utils import average_rating
from django.contrib import messages
from django.utils import timezone

def index(request):
    return render(request, "reviews/base.html")


def review_edit(request, book_pk, review_pk=None):
    book = get_object_or_404(Book, pk=book_pk)
    if review_pk is not None:
        review = get_object_or_404(Review, pk=review_pk)
    else:
        review = None

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            updated_review = form.save(commit=False)
            updated_review.book = book
            if review is None:
                messages.success(request, "Review for {} was created.".format(book.title))
            else:
                updated_review.date_edited = timezone.now()
                messages.success(request, "Review{} was updated".format(book.title))
            updated_review.save()
            return redirect("book_details", book.pk)
    else:
        form = ReviewForm(instance=review)

    return render(request, "reviews/instance-form.html",
        {"form": form, "instance": review, "model_type": "Review", "related_instance": Book,
         "related_model_type": "Book"})


def publisher_edit(request, pk=None):
    if pk is not None:
        publisher = get_object_or_404(Publisher, pk=pk)
    else:
        publisher = None

    if request.method == "POST":
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            updated_publisher = form.save()
            if publisher is None:
                messages.success(request, "Publisher {} was created.".format(updated_publisher))
            else:
                messages.success(request, "Publisher {} was updated.".format(updated_publisher))
            return redirect("publisher_edit", updated_publisher.pk)
    else:
        form = PublisherForm(instance=publisher)
    return render(request, "reviews/instance-form.html",
                  {"form": form, "instance": publisher, "model_type": "Publisher"})


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


def book_search(request):
    search_text = request.GET.get("search", "")
    form = SearchFrom(request.GET)
    results = set()
    if form.is_valid() and form.cleaned_data['search']:
        search = form.cleaned_data["search"]
        print(search)
        search_in = form.cleaned_data.get("search_in") or 'title'
        print(search_in)

        if search_in == 'title':
            books_fetched = Book.objects.filter(title__icontains=search)
            for book in books_fetched:
                results.add(book)
        else:
            contributed_fetched = Contributor.objects.filter(
                Q(first_names__icontains=search_text) | Q(last_names__icontains=search)
            )
            for contributor in contributed_fetched:
                for book in contributor.book_set.all():
                    results.add(book)

    return render(request, 'reviews/searchResult.html', {
        "form": form, "search_text": search_text, "result": results
    })
