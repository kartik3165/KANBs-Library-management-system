# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from .models import Book, Student, BookIssue, Fine, ActivityLog
from django.db.models import Q

# Book Views
def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')
        quantity = int(request.POST.get('quantity', 1))
        category = request.POST.get('category')
        publication_year = int(request.POST.get('publication_year'))
        
        book = Book.objects.create(
            title=title,
            author=author,
            isbn=isbn,
            quantity=quantity,
            available_quantity=quantity,
            category=category,
            publication_year=publication_year
        )
        
        ActivityLog.objects.create(
            activity_type='book_added',
            description=f'Added book: {book.title}',
            performed_by=request.POST.get('librarian_name', 'Unknown')
        )
        
        messages.success(request, 'Book added successfully!')
        return redirect('library:book_list')
    
    return render(request, 'library/add_book.html')

def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.isbn = request.POST.get('isbn')
        book.category = request.POST.get('category')
        book.publication_year = int(request.POST.get('publication_year'))
        
        new_quantity = int(request.POST.get('quantity'))
        quantity_difference = new_quantity - book.quantity
        book.quantity = new_quantity
        book.available_quantity += quantity_difference
        
        book.save()
        
        ActivityLog.objects.create(
            activity_type='book_updated',
            description=f'Updated book: {book.title}',
            performed_by=request.POST.get('librarian_name', 'Unknown')
        )
        
        messages.success(request, 'Book updated successfully!')
        return redirect('library:book_list')
    
    return render(request, 'library/edit_book.html', {'book': book})

def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        
        ActivityLog.objects.create(
            activity_type='book_deleted',
            description=f'Deleted book: {book_title}',
            performed_by=request.POST.get('librarian_name', 'Unknown')
        )
        
        messages.success(request, 'Book deleted successfully!')
        return redirect('library:book_list')
    
    return render(request, 'library/delete_book.html', {'book': book})

# Student Views
def student_list(request):
    students = Student.objects.all()
    return render(request, 'library/student_list.html', {'students': students})

def add_student(request):
    if request.method == 'POST':
        student = Student.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            student_id=request.POST.get('student_id'),
            email=request.POST.get('email'),
            department=request.POST.get('department'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address')
        )
        
        ActivityLog.objects.create(
            activity_type='student_added',
            description=f'Added student: {student.get_full_name()}',
            performed_by=request.POST.get('librarian_name', 'Unknown')
        )
        
        messages.success(request, 'Student added successfully!')
        return redirect('library:student_list')
    
    return render(request, 'library/add_student.html')

# Book Issue Views
def issue_book(request):
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=request.POST.get('book_id'))
        student = get_object_or_404(Student, pk=request.POST.get('student_id'))
        
        if book.available_quantity <= 0:
            messages.error(request, 'Book is not available for issue!')
            return redirect('library:issued_books_list')
        
        issue_date = timezone.now().date()
        due_date = issue_date + timedelta(days=14)  # 2 weeks lending period
        
        book_issue = BookIssue.objects.create(
            book=book,
            student=student,
            issue_date=issue_date,
            due_date=due_date,
            status='issued'
        )
        
        book.available_quantity -= 1
        book.save()
        
        ActivityLog.objects.create(
            activity_type='book_issued',
            description=f'Book {book.title} issued to {student.get_full_name()}',
            performed_by=request.POST.get('librarian_name', 'Unknown')
        )
        
        messages.success(request, 'Book issued successfully!')
        return redirect('library:issued_books_list')
    
    books = Book.objects.filter(available_quantity__gt=0)
    students = Student.objects.all()
    return render(request, 'library/issue_book.html', {
        'books': books,
        'students': students
    })

def return_book(request, issue_id):
    book_issue = get_object_or_404(BookIssue, pk=issue_id)
    
    if request.method == 'POST':
        book_issue.return_date = timezone.now().date()
        book_issue.status = 'returned'
        book_issue.save()
        
        book_issue.book.available_quantity += 1
        book_issue.book.save()
        
        # Calculate and create fine if book is overdue
        if book_issue.is_overdue():
            fine_amount = book_issue.calculate_fine()
            Fine.objects.create(
                book_issue=book_issue,
                amount=fine_amount
            )
        
        ActivityLog.objects.create(
            activity_type='book_returned',
            description=f'Book {book_issue.book.title} returned by {book_issue.student.get_full_name()}',
            performed_by=request.POST.get('librarian_name', 'Unknown')
        )
        
        messages.success(request, 'Book returned successfully!')
        return redirect('library:issued_books_list')
    
    return render(request, 'library/return_book.html', {'book_issue': book_issue})

def issued_books_list(request):
    issued_books = BookIssue.objects.filter(
        Q(status='issued') | Q(status='overdue')
    ).order_by('-issue_date')
    
    # Update status for overdue books
    for issue in issued_books:
        if issue.is_overdue() and issue.status != 'overdue':
            issue.status = 'overdue'
            issue.save()
    
    return render(request, 'library/issued_books_list.html', {
        'issued_books': issued_books
    })

# Fine Views
def fine_list(request):
    fines = Fine.objects.filter(payment_status='pending')
    return render(request, 'library/fine_list.html', {'fines': fines})

def collect_fine(request, fine_id):
    fine = get_object_or_404(Fine, pk=fine_id)
    
    if request.method == 'POST':
        fine.payment_status = 'paid'
        fine.payment_date = timezone.now().date()
        fine.save()
        
        ActivityLog.objects.create(
            activity_type='fine_collected',
            description=f'Collected fine of ₹{fine.amount} from {fine.book_issue.student.get_full_name()}',
            performed_by=request.POST.get('librarian_name', 'Unknown')
        )
        
        messages.success(request, 'Fine collected successfully!')
        return redirect('library:fine_list')
    
    return render(request, 'library/collect_fine.html', {'fine': fine})

# Activity Log View
def activity_log(request):
    activities = ActivityLog.objects.all().order_by('-created_at')
    return render(request, 'library/activity_log.html', {'activities': activities})
