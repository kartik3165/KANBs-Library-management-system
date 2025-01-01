from django.contrib import admin
from .models import Department , Book_category , Book , Student
# Register your models here.

admin.site.register(Department)
admin.site.register(Book_category)
admin.site.register(Book)
admin.site.register(Student)