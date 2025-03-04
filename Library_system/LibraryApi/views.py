from django.shortcuts import render , HttpResponse , redirect , get_object_or_404
from django.contrib import messages
from LibraryApp.models import *
from LibraryApi.serializers import *
from datetime import datetime , timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from decimal import Decimal
import json 
from django.http import JsonResponse
from itertools import groupby
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import (
    BookSerializer, BookCategorySerializer, DepartmentSerializer, 
    StudentSerializer, BookIssueSerializer, FineSerializer, TransactionSerializer
)

@login_required(login_url='login')
@api_view(['GET'])
def home(request):
    if request.method == 'GET':
        stud_count = Student.objects.count()
        return Response({'stud_count' : stud_count})

class BookCategoryViewSet(viewsets.ModelViewSet):
    queryset = Book_category.objects.all()
    serializer_class = BookCategorySerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class BookIssueViewSet(viewsets.ModelViewSet):
    queryset = BookIssue.objects.all()
    serializer_class = BookIssueSerializer

class FineViewSet(viewsets.ModelViewSet):
    queryset = Fine.objects.all()
    serializer_class = FineSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
