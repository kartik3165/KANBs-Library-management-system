from django.shortcuts import render , HttpResponse , redirect , get_object_or_404
from django.contrib import messages
from . models import Department , Student , Book , Book_category , BookIssue , Fine , Transaction
from datetime import datetime , timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from decimal import Decimal
import json 
from django.http import JsonResponse
from itertools import groupby

# Create your views here.
@login_required(login_url='login')
def home(request):
    stud_count = Student.objects.all().count()
    print('count' , stud_count)
    return render(request, 'index.html' , {'stud_count' : stud_count })

def manage_book(request):
    category = Book_category.objects.all()
    books_data = Book.objects.all().order_by('-id')[:5]
    return render(request , 'manage_book.html' , {'category_data' : category ,'books' : books_data})

def add_book(request):
    if request.method == 'POST':
        ti = request.POST['title']
        aut = request.POST['author']
        book_qau = request.POST['book_qauntity']
        cat = request.POST['dept_spinner']
        pub_year = request.POST['pub_year']

        Book.objects.create(
            title = ti ,
            author = aut,
            quantity = book_qau ,
            available_quantity = book_qau,
            category = cat ,
            publication_year = pub_year 
        )
        return redirect('manage_book')
    return HttpResponse('Book Not added')

def delete_book(request , id):
    book = Book.objects.get(id = id )
    book.delete()
    return redirect('book_table')

def book_table(request):
    book_data = Book.objects.all()
    return render(request , 'book_table.html' , {'book_data' : book_data})

def load_book(request, id):
    dept_data = Book_category.objects.all()
    print(dept_data)
    book_data = Book.objects.all()
    book = Book.objects.get(id=id)  
    return render(request, 'book_table.html', {'data': book, 'book_data': book_data, 'dept_data': dept_data})

def update_book(request , id):
    book = Book.objects.get(id = id)
    if request.method == 'POST':
        ti = request.POST['title']
        aut = request.POST['author']
        book_qau = request.POST['book_qauntity']
        pub_year = request.POST['pub_year']

    book.title = ti
    book.author = aut
    book.quantity = book_qau
    book.available_quantity = book_qau # - issue_quantity 
    book.publication_year = pub_year
    book.updated_at = datetime.now()
    book.save()
    return redirect('book_table')

def manage_student(request):
    dept_data = Department.objects.all()
    student_data = Student.objects.all().order_by('-id')[:5]
    return render(request , 'manage_student.html' , {'dept_data' : dept_data , 'student_data' : student_data})

def add_student(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        dept = request.POST['dept_spinner']
        ph = request.POST['ph_no']

        Student.objects.create(
            name = name ,
            email = email , 
            department = dept ,
            phone = ph
        )
        return redirect('manage_student')
    return HttpResponse('Student Not added')

def delete_student(request , id):
    student = Student.objects.get(id = id )
    student.delete()
    return redirect('student_table')

def student_table(request):
    student_data = Student.objects.all()
    student_with_fine = []
    for student in student_data:
        fine = get_fine(student.id) 
        student_with_fine.append({'student': student, 'fine': fine})  
    return render(request, 'student_table.html', {'student_with_fine': student_with_fine})

def load_student(request, id):
    dept_data = Department.objects.all()
    student_data = Student.objects.all()
    student = Student.objects.get(id=id)
    return render(request, 'student_table.html', {'data': student, 'student_data': student_data, 'dept_data': dept_data})

def update_student(request , id):
    student = Student.objects.get(id = id)
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        ph = request.POST['ph_no']

    student.name = name
    student.email = email
    student.phone = ph
    student.updated_at = datetime.now()
    student.save()
    return redirect('student_table')

def issue_book(request):
    student_data = Student.objects.all()
    book_data = Book.objects.all()
    issue_data = BookIssue.objects.filter(return_date__isnull = True).order_by('-id')[:5]
    return render(request , 'issue_book.html' , { 'student_data' : student_data , 'book_data' : book_data , 'issue_data' : issue_data})

def issue_book_form(request):
    if request.method == 'POST':
        b_id = request.POST['book_id']
        s_id = request.POST['student_id']

        issue_date = datetime.now().date()
        due_date = issue_date + timedelta(days=2)
        student = Student.objects.get(id = s_id)
        book = Book.objects.get(id = b_id)

        BookIssue.objects.create(
            book = book ,
            student = student ,
            issue_date = issue_date ,
            due_date = due_date
        )

        book.available_quantity -=1
        book.save()

        return redirect('issue_book')
    return HttpResponse('book did not issued')

def issue_table(request):
    issue_data = BookIssue.objects.filter(return_date__isnull = True)
    return render(request , 'issue_table.html' , { 'issue_data' : issue_data })

def return_book(request):
    issue_data = BookIssue.objects.filter(return_date__isnull = False).order_by('-id')[:5]
    return render(request , 'return_book.html' , {'issue_data' : issue_data})

def get_issue_data(request): #gpt help
    if request.method == 'POST':
        data = json.loads(request.body)
        stud_id = data.get('student_id')
        
        # Retrieve all book issues for the given student ID
        issue_data = BookIssue.objects.filter(student__id=stud_id)
        
        # Prepare the issue data as a list of dictionaries, excluding returned books
        issues = []
        for issue in issue_data:
            if issue.return_date is None:  # Only include books that are not returned
                issues.append({
                    'id': issue.id,
                    'book_title': issue.book.title,
                    'issue_date': issue.issue_date.strftime('%Y-%m-%d'),
                    'due_date': issue.due_date.strftime('%Y-%m-%d'),
                })
        
        # Return the issue data as JSON
        return JsonResponse({'issue_data': issues})
    else:
        # Render the form if it's a GET request (optional)
        return render(request, 'issue_data_form.html')

def return_order(request, id):
    try:
        issue_book = BookIssue.objects.get(id=id)
        book_info = issue_book.book 

        if issue_book.return_date:
            return HttpResponse("Book has already been returned.")

        if issue_book.is_overdue():
            days_overdue = (datetime.now().date() - issue_book.due_date).days
            fine_amount = days_overdue * 6 

            Fine.objects.create(
                book_issue=issue_book,
                amount=fine_amount,
                payment_status='pending'
            )
            issue_book.status = 'overdue'
        else:
            issue_book.status = 'returned'

        # Update the return date
        issue_book.return_date = datetime.now().date()
        issue_book.save()

        # Update the available quantity of the book
        book_info.available_quantity += 1
        book_info.save()

        return HttpResponse("Book returned successfully.")
    except BookIssue.DoesNotExist:
        return HttpResponse("Book issue record not found.", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

def return_table(request):
    issue_data = BookIssue.objects.filter(return_date__isnull = False)
    return render(request , 'return_table.html' , {'issue_data' : issue_data})
    
def fine_table(request):
    from itertools import groupby
    from django.db.models import Sum

    transactions = Transaction.objects.all().select_related('book_issue__student', 'book_issue__book').order_by('book_issue__student_id', '-payment_date')
    grouped_transactions = []

    for key, group in groupby(transactions, key=lambda x: x.book_issue.student.id):
        student_transactions = list(group)

        # Debug: Print student and their transactions
        print(f"Student ID: {key}, Transactions: {student_transactions}")

        # Calculate total fine
        total_fine = sum([transaction.amount for transaction in student_transactions])
        print(f"Total Fine for Student {key}: {total_fine}")

        # Calculate paid fine
        paid_fine = sum([transaction.amount for transaction in student_transactions if transaction.payment_date is not None])
        print(f"Paid Fine for Student {key}: {paid_fine}")

        # Calculate remaining fine
        remaining_fine = total_fine - paid_fine
        print(f"Remaining Fine for Student {key}: {remaining_fine}")

        grouped_transactions.append({
            'student_id': key,
            'student_name': student_transactions[0].book_issue.student.name,
            'total_fine': total_fine,
            'paid_fine': paid_fine,
            'remaining_fine': remaining_fine,
            'transactions': student_transactions
        })
    
    return render(request, 'fine_table.html', {'grouped_transactions': grouped_transactions})

def fines(request):
    issue_data = Fine.objects.all()
    data_withFine = []
    for item in issue_data:
        fine_amount = item.amount  # Assuming fine amount is stored in Fine model
        data_withFine.append({
            'book_issue': item.book_issue,
            'fine': fine_amount,
        })

    return render(request, 'fine.html', {'data': data_withFine})

def collect_fine(request, issue_id):
    book_issue = get_object_or_404(BookIssue, id = issue_id)
    fine = Fine.objects.filter(book_issue=book_issue).first()

    if not fine:
        messages.error(request, "Fine not found for this issue.")
        return redirect('some_view')  # Redirect to an appropriate view

    if request.method == 'POST':
        payment_amount = request.POST.get('payment_amount')

        try:
            payment_amount = Decimal(payment_amount)
        except:
            messages.error(request, "Invalid amount.")
            return redirect('fines', issue_id=issue_id)

        if payment_amount <= 0:
            messages.error(request, "Amount must be greater than zero.")
            return redirect('fines', issue_id=issue_id)

        # Record the payment in the Transaction table
        transaction = Transaction(
            book_issue=book_issue,
            amount=payment_amount
        )
        transaction.save()

        # Deduct the payment from the fine
        fine.amount -= payment_amount
        fine.save()

        # If fine is fully paid, mark as paid
        if fine.amount <= 0:
            fine.payment_status = 'paid'
            fine.save()

        messages.success(request, f"Payment of {payment_amount} recorded successfully.")
        return redirect('fines')

    # Render the form to collect fine
    return render(request, 'fines.html', {'book_issue': book_issue, 'fine': fine})

def get_fine(id):
    try:
        fine_info = Fine.objects.filter(book_issue__student_id = id)
        total_fine = Decimal('0.00')

        for fine in fine_info:
            total_fine += fine.amount

        if fine_info.exists():
            return total_fine
        else:
            return '0.00'
        
    except Fine.DoesNotExist:
        return '0.00'
    
def get_fine_for_issueID(id):
    try:
        fine_info = Fine.objects.filter(book_issue__student_id = id)
        total_fine = Decimal('0.00')   

        for fine in fine_info:
            print(fine.amount)

        if fine_info.exists():
            return total_fine
        else:
            return '0.00'
        
    except Fine.DoesNotExist:
        return '0.00'
    
def calculate_fine(book_issue):
    # Calculate fine based on overdue days
    if book_issue.due_date < datetime.now().date() and not book_issue.return_date:
        days_overdue = (datetime.now().date() - book_issue.due_date).days
        return Decimal('6.00') * days_overdue
    return Decimal('0.00')

def create_or_update_fine(book_issue_id):
    try:
        book_issue = BookIssue.objects.get(id=book_issue_id)
        fine_amount = calculate_fine(book_issue)

        # Create or update the Fine record
        fine, created = Fine.objects.update_or_create(
            book_issue=book_issue,
            defaults={'amount': fine_amount}
        )
        return fine
    except BookIssue.DoesNotExist:
        # Handle case where BookIssue does not exist
        return None

def login_view(request):
    """
    Handle user login with built-in Django authentication
    """
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    """
    Handle new user registration
    """
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})