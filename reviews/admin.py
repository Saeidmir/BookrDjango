from django.contrib import admin
from django.contrib.admin import ModelAdmin
# Register your models here.
from django.shortcuts import get_object_or_404

from reviews.models import Review, Book, BookContributor, Contributor, Publisher


class ContributeAdmin(ModelAdmin):
    list_display = ('last_names', 'first_names')
    list_filter = ('last_names',)


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn13')
    list_filter = ('publisher', 'publication_date')
    date_hierarchy = 'publication_date'
    search_fields = ('title', 'isbn', 'publisher__name')

    def isbn13(self, obj):
        """ '9780316769174' => '978-0-31-676917-4' """
        return "{}-{}-{}-{}-{}".format(
            obj.isbn[0:3], obj.isbn[3:4], obj.isbn[4:6], obj.isbn[6:12], obj.isbn[12:13]
        )
    def get_publisher(self,obj):
        return  obj.publisher.name


class ReviewAdmin(admin.ModelAdmin):
    # fields = ('content', 'rating', 'creator', 'book')
    fieldsets = (('Linkage', {'fields': ('creator', 'book')}),
                 ('Review content',
                  {'fields': ('content', 'rating')}))


admin.site.register(Publisher)
admin.site.register(Book, BookAdmin)
admin.site.register(BookContributor)
admin.site.register(Contributor, ContributeAdmin)
admin.site.register(Review, ReviewAdmin)
