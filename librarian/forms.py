from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#from phonenumber_field.modelfields import PhoneNumberField
from django.forms import ModelForm
from .models import Book,Student,Librarian,IssueData

class SignUpForm(UserCreationForm):
	librarian_name = forms.CharField(
		label='Librarian Name',
		max_length=50,
		help_text='Enter your full name'
	)
	
	def __init__(self, *args, **kwargs):
		super(UserCreationForm, self).__init__(*args, **kwargs)
		self.fields['username'].help_text = 'Please enter your Username <strong>Eg:gaikwadabhishek </strong>'

	class Meta:
		model = User
		fields = ('username', 'librarian_name' , 'password1', 'password2', )
		widgets = {
			'username': forms.TextInput(),
			'librarian_name':forms.TextInput(),
			'password1':forms.TextInput(),
			'password2':forms.TextInput()
		}

class AddStudentForm(forms.ModelForm):
	class Meta:
		model = Student
		exclude=()

'''
class AddStudentForm(forms.Form):
	student_name = forms.CharField(required=True,help_text='Enter Name of the Student')
	student_id = forms.CharField(required=True,help_text='Enter ID of the Student')
	student_email = forms.EmailField(max_length=254,  required=True, help_text='Inform a valid email address.')
	student_phno = forms.CharField(required=True,help_text='Enter a valid phone number of student')
'''
class AddBookForm(forms.ModelForm):
	'''title = forms.CharField(required=True,help_text='Enter Name of the Book')
	book_id = forms.CharField(required=True,help_text='Enter ID of the Book')
	author = forms.CharField(required=True,help_text='Enter author of the Book')
	publisher = forms.CharField(required=True,help_text='Enter publisher of the Book')'''
	class Meta:
		model=Book
		exclude=()

class IssueBookForm(forms.ModelForm):
	
	class Meta:
		model=IssueData
		exclude=()
	

