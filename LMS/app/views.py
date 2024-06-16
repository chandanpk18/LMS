from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required,  user_passes_test
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils import timezone
from .models import Book, IssuedBook
from django.contrib.auth.models import User

def is_admin(user):
    return user.is_superuser

@login_required(login_url='login')
@user_passes_test(is_admin)
def issue_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        user_id = int(request.POST['user_id'])
        user = get_object_or_404(User, id=user_id)
        due_date = timezone.now().date() + timedelta(days=10)

        if book.available_copies > 0:
            IssuedBook.objects.create(user=user, book=book, isbn=book.isbn, due_date=due_date)
            book.available_copies -= 1
            book.save()
            return redirect('admin_dashboard')
        else:
            return render(request, 'issue_book.html', {'book': book, 'error': 'No copies available'})

    users = User.objects.filter(is_superuser=False)
    return render(request, 'issue_book.html', {'book': book, 'users': users})

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='login')
def signout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    return redirect('user_dashboard')

@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_dashboard(request):
    books = Book.objects.all()
    issued_books = IssuedBook.objects.filter(is_returned=False)
    return render(request, 'admin_dashboard.html', {'books': books, 'issued_books': issued_books})

@login_required(login_url='login')
def user_dashboard(request):
    issued_books = IssuedBook.objects.filter(user=request.user, is_returned=False)
    books = Book.objects.all()
    return render(request, 'user_dashboard.html', {'issued_books': issued_books,'books':books})

@login_required(login_url='login')
@user_passes_test(is_admin)
def add_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        isbn = request.POST['isbn']
        author = request.POST['author']
        category = request.POST['category']
        total_copies = int(request.POST['total_copies'])
        available_copies = total_copies
        location = request.POST['location']
        Book.objects.create(title=title, isbn=isbn, author=author, category=category, total_copies=total_copies, available_copies=available_copies, location=location)
        return redirect('admin_dashboard')
    return render(request, 'add_book.html')

@login_required(login_url='login')
@user_passes_test(is_admin)
def return_book(request, issued_book_id):
    issued_book = get_object_or_404(IssuedBook, id=issued_book_id)
    issued_book.is_returned = True
    issued_book.save()
    book = issued_book.book
    book.available_copies += 1
    book.save()
    return redirect('admin_dashboard')

@login_required(login_url='login')

def search_books(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        category = request.GET.get('category')
        books = Book.objects.all()
        if query:
            books = books.filter(title__icontains=query)
        if category:
            books = books.filter(category=category)
        return render(request, 'user_dashboard.html', {'books': books})
