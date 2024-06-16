from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Book(models.Model):
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField()
    location = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.title

class IssuedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} issued to {self.user.username}"

    @property
    def fine_amount(self):
        if self.is_returned:
            return 0
        today = timezone.now().date()
        if today > self.due_date:
            overdue_days = (today - self.due_date).days
            return overdue_days * 10
        return 0


class users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150)
    password = models.TextField(max_length=20)

    def __str__(self):
        return self.username