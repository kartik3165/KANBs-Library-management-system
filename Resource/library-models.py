from django.db import models
from decimal import Decimal
from datetime import datetime, timedelta

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    quantity = models.IntegerField(default=1)
    available_quantity = models.IntegerField(default=1)
    category = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class BookIssue(models.Model):
    ISSUE_STATUS_CHOICES = [
        ('issued', 'Issued'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    issue_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=ISSUE_STATUS_CHOICES, default='issued')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.book.title} - {self.student.get_full_name()}"

    def is_overdue(self):
        if not self.return_date and self.due_date < datetime.now().date():
            return True
        return False

    def calculate_fine(self):
        if not self.is_overdue():
            return Decimal('0.00')
        days_overdue = (datetime.now().date() - self.due_date).days
        return Decimal('10.00') * days_overdue  # ₹10 per day fine

class Fine(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('waived', 'Waived'),
    ]

    book_issue = models.ForeignKey(BookIssue, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Fine for {self.book_issue}"

class ActivityLog(models.Model):
    ACTIVITY_CHOICES = [
        ('book_added', 'Book Added'),
        ('book_updated', 'Book Updated'),
        ('book_deleted', 'Book Deleted'),
        ('student_added', 'Student Added'),
        ('student_updated', 'Student Updated'),
        ('student_deleted', 'Student Deleted'),
        ('book_issued', 'Book Issued'),
        ('book_returned', 'Book Returned'),
        ('fine_collected', 'Fine Collected'),
    ]

    activity_type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    description = models.TextField()
    performed_by = models.CharField(max_length=100)  # Now storing just the name of who performed the action
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.activity_type} - {self.created_at}"
