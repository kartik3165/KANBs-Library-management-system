from django.db import models
from decimal import Decimal
from datetime import datetime , timedelta

# Create your models here.

class Book_category(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name
    
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    available_quantity = models.IntegerField(default=1)
    category = models.ForeignKey(Book_category, related_name='category', on_delete=models.CASCADE, default='General')
    publication_year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author}"
    
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    phone = models.IntegerField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True , editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {self.id}"
    