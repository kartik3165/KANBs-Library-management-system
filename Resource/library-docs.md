# Library Management System Implementation Guide

## Table of Contents
- [Project Setup](#project-setup)
- [Database Configuration](#database-configuration)
- [Models Implementation](#models-implementation)
- [URL Configuration](#url-configuration)
- [Views Implementation](#views-implementation)
- [Templates Structure](#templates-structure)
- [Static Files](#static-files)
- [Running the Project](#running-the-project)

## Project Setup

1. Create a new Django project:
```bash
django-admin startproject library_management
cd library_management
```

2. Create a new app:
```bash
python manage.py startapp library
```

3. Add 'library' to INSTALLED_APPS in settings.py:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'library',  # Add this line
]
```

## Database Configuration

1. Configure your database in settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

2. Create migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Models Implementation

Create the following models in `library/models.py`:

```python
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

```

## URL Configuration

1. Update `library_management/urls.py`:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library.urls')),
]
```

2. Create `library/urls.py`:
```python
# urls.py
from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    # Book URLs
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
    
    # Student URLs
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/<int:pk>/edit/', views.edit_student, name='edit_student'),
    path('students/<int:pk>/delete/', views.delete_student, name='delete_student'),
    
    # Book Issue URLs
    path('issue-book/', views.issue_book, name='issue_book'),
    path('return-book/<int:issue_id>/', views.return_book, name='return_book'),
    path('issued-books/', views.issued_books_list, name='issued_books_list'),
    
    # Fine URLs
    path('fines/', views.fine_list, name='fine_list'),
    path('collect-fine/<int:fine_id>/', views.collect_fine, name='collect_fine'),
    
    # Activity Log URL
    path('activity-log/', views.activity_log, name='activity_log'),
]
```

## Templates Structure

Create the following directory structure:
```
library/
    templates/
        library/
            base.html
            book_list.html
            add_book.html
            edit_book.html
            delete_book.html
            student_list.html
            add_student.html
            edit_student.html
            delete_student.html
            issue_book.html
            return_book.html
            issued_books_list.html
            fine_list.html
            collect_fine.html
            activity_log.html
```

### Base Template (base.html)
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Library Management System{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'library:book_list' %}">Library Management</a>
            <div class="navbar-nav">
                <a class="nav-link" href="{% url 'library:book_list' %}">Books</a>
                <a class="nav-link" href="{% url 'library:student_list' %}">Students</a>
                <a class="nav-link" href="{% url 'library:issued_books_list' %}">Issued Books</a>
                <a class="nav-link" href="{% url 'library:fine_list' %}">Fines</a>
                <a class="nav-link" href="{% url 'library:activity_log' %}">Activity Log</a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}

        {% block content %}
        {% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

## Sample Template Implementation

### Book List Template (book_list.html)
```html
{% extends 'library/base.html' %}

{% block title %}Books - Library Management{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2>Books</h2>
    <a href="{% url 'library:add_book' %}" class="btn btn-primary">Add Book</a>
</div>

<table class="table table-striped">
    <thead>
        <tr>
            <th>Title</th>
            <th>Author</th>
            <th>ISBN</th>
            <th>Available</th>
            <th>Total</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for book in books %}
        <tr>
            <td>{{ book.title }}</td>
            <td>{{ book.author }}</td>
            <td>{{ book.isbn }}</td>
            <td>{{ book.available_quantity }}</td>
            <td>{{ book.quantity }}</td>
            <td>
                <a href="{% url 'library:edit_book' book.pk %}" class="btn btn-sm btn-warning">Edit</a>
                <a href="{% url 'library:delete_book' book.pk %}" class="btn btn-sm btn-danger">Delete</a>
            </td>
        </tr>
        {% empty %}
        <tr>
            <td colspan="6" class="text-center">No books available.</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```

## Static Files

1. Create static files directory structure:
```
library/
    static/
        library/
            css/
                styles.css
            js/
                scripts.js
```

2. Configure static files in settings.py:
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'library' / 'static',
]
```

## Running the Project

1. Create a superuser for admin access:
```bash
python manage.py createsuperuser
```

2. Register models in admin.py:
```python
from django.contrib import admin
from .models import Book, Student, BookIssue, Fine, ActivityLog

admin.site.register(Book)
admin.site.register(Student)
admin.site.register(BookIssue)
admin.site.register(Fine)
admin.site.register(ActivityLog)
```

3. Run the development server:
```bash
python manage.py runserver
```

## Features Implementation Checklist

- [ ] Book Management
  - [ ] Add new books
  - [ ] Update book quantities
  - [ ] Delete books
  - [ ] View book list

- [ ] Student Management
  - [ ] Add new students
  - [ ] Update student information
  - [ ] Delete students
  - [ ] View student list

- [ ] Book Issue System
  - [ ] Issue books to students
  - [ ] Return books
  - [ ] Track due dates
  - [ ] Handle overdue books

- [ ] Fine Management
  - [ ] Calculate fines for overdue books
  - [ ] Collect fines
  - [ ] Track payment status

- [ ] Activity Logging
  - [ ] Log all system activities
  - [ ] View activity history

## Security Considerations

1. Always validate input data
2. Implement proper user authentication
3. Use CSRF protection in forms
4. Sanitize data before display
5. Implement proper access controls

## Best Practices

1. Follow PEP 8 coding style
2. Write meaningful commit messages
3. Document your code
4. Write unit tests
5. Regularly backup your database
6. Use meaningful variable names
7. Keep your dependencies updated

## Troubleshooting

Common issues and solutions:

1. Database migrations:
```bash
python manage.py makemigrations --dry-run  # Check migrations before applying
python manage.py showmigrations  # See migration status
python manage.py migrate --plan  # See what migrations will be applied
```

2. Static files not loading:
- Check STATIC_URL and STATICFILES_DIRS in settings.py
- Run `python manage.py collectstatic`
- Ensure proper template tags are used

3. Template not found:
- Check template directory structure
- Ensure app is in INSTALLED_APPS
- Verify template name and location

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [Python PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
