from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date,timedelta
from django.core.urlresolvers import reverse
#from phonenumber_field.modelfields import PhoneNumberField

class Librarian(models.Model):
	user = models.OneToOneField(User,on_delete = models.CASCADE)
	librarian_name = models.CharField(max_length = 50)
	def __str__(self):
		return self.librarian_name

class Student(models.Model):
    student_name = models.CharField(max_length = 50)
    student_id = models.CharField(max_length=14)
    student_email = models.EmailField(max_length=254)
    student_phno = models.CharField(max_length = 15)
    def __str__(self):
        return self.student_name

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
	if created:
		Librarian.objects.create(user=instance)
	instance.librarian.save()

class Book(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    """
    book_id = models.CharField(primary_key=True, max_length=50, help_text="Unique ID for this particular book across whole library")
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, null=True)
    publisher = models.CharField(max_length=200, null=True)
    student_issued = Student()
    LOAN_STATUS = (
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    

    status= models.CharField(max_length=1, choices=LOAN_STATUS, default='a', help_text='Book availability')

    '''def get_absolute_url(self):
        
        Returns the url to access a particular book instance.
        
        return reverse('book-detail', args=[str(self.book_id)])'''

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title
        
class IssueData(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True) 
    #imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True,default=date.today()+timedelta(days=15))
    borrower = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True, blank=True)
    #fine=model.IntegerField(on_delete=models.SET_NULL,default=0)
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    

    
    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)   

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s (%s)' % (self.id,self.book.title)