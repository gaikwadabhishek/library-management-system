from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.conf.urls import include
from django.template import loader
from .models import Student
from django.http import Http404
from .forms import SignUpForm,AddStudentForm,AddBookForm,IssueBookForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from .models import Book,Student,Librarian
# Create your views here.
from django.views import generic
@login_required
def home(request):
    return render(request, 'home.html')

def signup_success(request):
    return render(request,'signup_success.html')

def addbook_success(request):
    return render(request,'addbook_success.html')

def addstudent_success(request):
    return render(request,'addstudent_success.html')

def issuebook_success(request):
	return render(request,'issuebook_success.html')

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()
			user.student.librarian_name = form.cleaned_data.get('librarian_name')
			#user.student.email = form.cleaned_data.get('email')
			#user.student.phone_number = form.cleaned_data.get('phone_number')
			user.refresh_from_db()
			user.save()
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=user.username, password=raw_password)
			login(request, user)
			return redirect('signup_success')
	else:
		form = SignUpForm()
	return render(request, 'signup.html', {'form': form})

def addbook(request):
	form = AddBookForm()
	if request.method=='POST':
		form = AddBookForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			form.save()
			return redirect('addbook_success')
		else:
			form = AddBookForm()
	return render(request,'addbook.html',{'form':form})


def add_student(request):
	form = AddStudentForm()
	if request.method=='POST':
		form = AddStudentForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			form.save()
			return redirect('addstudent_success')
		else:
			form = AddStudentForm()
	return render(request,'addstudent.html',{'form':form})
'''

def addbook(request):
	form = AddBookForm()
	if request.method=='POST':
		form = AddBookForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			student_name = cd.get('student_name ')
			student_id = cd.get('student_id')
			student_email = cd.get('student_email')
			student_phno = cd.get('student_phno')
			form.save()
	return render(request,'addstudent.html',{'form':form})
'''
def issuebook(request):
	form = IssueBookForm()
	if request.method=='POST':
		form = IssueBookForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			book = cd.get('book')
			borrower = cd.get('borrower')
			book.status = 'o'
			book.student_issued = borrower
			print(book.student_issued.student_name)
			book.save()
			form.save()
			return redirect('issuebook_success')
		else:
			form = IssueBookForm()
			
	return render(request,'issuebook.html',{'form':form})

class BookListView(generic.ListView):
    """
    Generic class-based view for a list of books.
    """
    model = Book
    paginate_by = 30
    
class BookDetailView(generic.DetailView):
    """
    Generic class-based detail view for a book.
    """
    model = Book

def detail(request, book_id):
    user = request.user
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'book-detail.html', {'book': book})

def index(request):
	all_book = list(Book.objects.all())
	print(all_book)
	return render(request,'index.html',{'all_book':all_book})
