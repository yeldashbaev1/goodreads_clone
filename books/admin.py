from django.contrib import admin
from books.models import Book, Author, BookAuthor, BookReview


class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'isbn')
    list_display = ('title', 'description', 'isbn')


class AuthorAdmin(admin.ModelAdmin):
    pass


class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ('author', 'book')


class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'stars_given', 'book')


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
