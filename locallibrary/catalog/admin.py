from django.contrib import admin
from catalog.models import Author,Book,Genre,BookInstance

# admin.site.register(Author)
# admin.site.register(Book)
# admin.site.register(BookInstance)
admin.site.register(Genre)

class BookInline(admin.TabularInline):
    model = Book
    
class Authoradmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name' , 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]



admin.site.register(Author,Authoradmin)

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back','book','id','borrower')
    fieldsets = (
        (None, {
            "fields": (
                'book', 'imprint', 'id'
            ),
        }),
        ('Acailability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )

class BookInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]