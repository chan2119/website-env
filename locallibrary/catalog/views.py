from .models import Book, Author, BookInstance, Genre
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # The 'all()' is implied by default.
    num_genres = Genre.objects.count()
    num_fiction_book = Book.objects.filter(title__contains="fiction").count()
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_books':num_books,
        'num_instances':num_instances,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors,
        'num_genres':num_genres,
        'num_fiction_book':num_fiction_book,
        'num_visits':num_visits
        },
    )

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'catalog/book_list.html'
    paginate_by = 2
    # def get_queryset(self):
    #     return Book.objects.filter(title__contains='fiction')

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class loanedBooksListView(LoginRequiredMixin,generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_lb.html"
    paginate_by = 10
    context_object_name = 'bookinstance_list'
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
