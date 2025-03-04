from django.urls import path, include
from rest_framework.routers import DefaultRouter
from LibraryApi.views import (
    BookViewSet, BookCategoryViewSet, DepartmentViewSet, StudentViewSet, 
    BookIssueViewSet, FineViewSet, TransactionViewSet
)

router = DefaultRouter()
router.register(r'book-categories', BookCategoryViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'books', BookViewSet)
router.register(r'students', StudentViewSet)
router.register(r'book-issues', BookIssueViewSet)
router.register(r'fines', FineViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
