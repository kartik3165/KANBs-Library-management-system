from django.urls import path 
from . import views

urlpatterns = [
    path('' , views.home , name = 'home'),
    path('auth' , views.auth , name = 'auth'),
    path('issue_book' , views.issue_book , name = 'issue_book'),
    path('issue_table' , views.issue_table , name = 'issue_table'),
    path('manage_book' , views.manage_book , name = 'manage_book'),
    path('book_table' , views.book_table , name = 'book_table'),

    path('manage_student' , views.manage_student , name = 'manage_student'),
    path('add-student', views.add_student , name = 'add-student'),
    path('student_table' , views.student_table , name = 'student_table'),
    path('delete_student/<int:id>', views.delete_student , name= 'delete_student'),
    path('load_student/<int:id>', views.load_student , name= 'load_student'),   
    path('update_student/<int:id>', views.update_student , name= 'update_student'),


    path('return_book' , views.return_book , name = 'return_book'),
    path('return_table' , views.return_table , name = 'return_table'),
    path('fine' , views.fine , name = 'fine'),
    path('fine_table' , views.fine_table , name = 'fine_table'),
]