from django.urls import path 
from . import views

urlpatterns = [
    path('' , views.home , name = 'home'),
    
    path('manage_book' , views.manage_book , name = 'manage_book'),
    path('book_table' , views.book_table , name = 'book_table'),
    path('add_book', views.add_book , name = 'add_book'),
    path('delete_book/<int:id>', views.delete_book , name= 'delete_book'),
    path('load_book/<int:id>', views.load_book , name= 'load_book'),   
    path('update_book/<int:id>', views.update_book , name= 'update_book'),

    
    path('manage_student' , views.manage_student , name = 'manage_student'),
    path('add-student', views.add_student , name = 'add-student'),
    path('student_table' , views.student_table , name = 'student_table'),
    path('delete_student/<int:id>', views.delete_student , name= 'delete_student'),
    path('load_student/<int:id>', views.load_student , name= 'load_student'),   
    path('update_student/<int:id>', views.update_student , name= 'update_student'),

    path('issue_book' , views.issue_book , name = 'issue_book'),
    path('issue_table' , views.issue_table , name = 'issue_table'),
    path('issue_book_form', views.issue_book_form , name = 'issue_book_form'),

    path('return_book' , views.return_book , name = 'return_book'),
    path('return_table' , views.return_table , name = 'return_table'),
    path('get_issue_data/' , views.get_issue_data , name = 'get_issue_data'),
    path('return_order/<int:id>' , views.return_order , name = 'return_order'),
    
    path('fines/', views.fines, name='fines'),
    path('fine_table' , views.fine_table , name = 'fine_table'),
    path('collect_fine/<int:issue_id>' , views.collect_fine , name = 'collect_fine')
]