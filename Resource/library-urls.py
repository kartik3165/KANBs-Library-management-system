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
