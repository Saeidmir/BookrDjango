from django.contrib import admin

# Register your models here.

from reviews.models import Review, Book, BookContributor, Contributor, Publisher

admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(BookContributor)
admin.site.register(Contributor)
admin.site.register(Review)
