from django.shortcuts import render , HttpResponse , redirect
from . models import Department , Student , Book , Book_category
from datetime import datetime , timedelta

# Create your views here.

def home(request):
    return render(request, 'index.html')

def auth(request):
    return render(request , 'auth.html')

def issue_book(request):
    return render(request , 'issue_book.html')

def issue_table(request):
    return render(request , 'issue_table.html')

def manage_book(request):
    return render(request , 'manage_book.html')

def manage_student(request):
    dept_data = Department.objects.all()
    student_data = Student.objects.all().order_by('-id')[:5]
    return render(request , 'manage_student.html',{'dept_data' : dept_data , 'student_data' : student_data})

def add_student(request):
    if request.method == 'GET':
        name = request.GET['name']
        email = request.GET['email']
        dept = request.GET['dept_spinner']
        ph = request.GET['ph_no']

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
    return redirect('manage_student')


def book_table(request):
    return render(request , 'book_table.html')

def student_table(request):
    student_data = Student.objects.all()
    return render(request , 'student_table.html',{'student_data' : student_data})

def load_student(request, id):
    dept_data = Department.objects.all()
    student_data = Student.objects.all()
    student = Student.objects.get(id=id)
    print("Student:", student)  # Check if the student object is correct
    print("Dept Data:", dept_data)  # Verify department data
    return render(request, 'student_table.html', {'data': student, 'student_data': student_data, 'dept_data': dept_data})

def update_student(request , id):
    student = Student.objects.get(id = id)
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        dept = request.POST['dept_spinner']
        ph = request.POST['ph_no']

    student.name = name
    student.email = email
    student.department = dept
    student.phone = ph
    student.updated_at = datetime.now()
    student.save()
    return redirect('student_table')


def return_book(request):
    return render(request , 'return_book.html')

def return_table(request):
    return render(request , 'return_table.html')

def fine_table(request):
    return render(request , 'fine_table.html')

def fine(request):
    return render(request , 'fine.html')

    