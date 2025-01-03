from django.shortcuts import render , HttpResponse , redirect
from . models import Department , Student , Book , Book_category , BookIssue , Fine
from datetime import datetime , timedelta
from decimal import Decimal
import json 
from django.http import JsonResponse

# Create your views here.

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
    return render(request , 'student_table.html',{'student_data' : student_data})

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
    issue_data = BookIssue.objects.all().order_by('-id')[:5]
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
    issue_data = BookIssue.objects.all()
    return render(request , 'issue_table.html' , { 'issue_data' : issue_data })

def return_book(request):
    return render(request , 'return_book.html' , {  })

def get_issue_data(request):
    if request.method == 'POST':
        # Parse the JSON data from the request body
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
        # Fetch the book issue record by ID
        issue_book = BookIssue.objects.get(id=id)
        book_info = issue_book.book  # Access the related book

        # Check if the book has already been returned
        if issue_book.return_date:
            return HttpResponse("Book has already been returned.", status=400)

        # Handle overdue case
        if issue_book.is_overdue():
            days_overdue = (datetime.now().date() - issue_book.due_date).days
            fine_amount = days_overdue * 6  # Assuming a fine of 6 units per day

            # Create a fine record
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
    return render(request , 'return_table.html')
    
def fine_table(request):
    return render(request , 'fine_table.html')

def fine(request):
    return render(request , 'fine.html')

def calculate_fine(book_issue):
    # Calculate fine based on overdue days
    if book_issue.due_date < datetime.now().date() and not book_issue.return_date:
        days_overdue = (datetime.now().date() - book_issue.due_date).days
        return Decimal('6.00') * days_overdue
    return Decimal('0.00')

# Example function for creating or updating fine
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
