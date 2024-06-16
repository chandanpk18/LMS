from django.contrib import admin
from .models import Book, IssuedBook, users

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'author', 'category', 'total_copies', 'available_copies')
    search_fields = ('title', 'author', 'isbn', 'category')
    list_filter = ('category',)

class IssuedBookAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'issue_date', 'due_date', 'is_returned')
    search_fields = ('book__title', 'user__username', 'book__isbn')
    list_filter = ('is_returned', 'issue_date', 'due_date')
    autocomplete_fields = ['book', 'user']

class usersAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')
    search_fields = ('username',)

admin.site.register(Book, BookAdmin)
admin.site.register(IssuedBook, IssuedBookAdmin)
admin.site.register(users, usersAdmin)
