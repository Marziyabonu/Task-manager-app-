from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    PRIORITY = [
        ("low", 'Low'),
        ("medium", 'Medium'),
        ("high", 'High'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS, default='new')
    priority = models.CharField(max_length=20, choices=PRIORITY, default='normal')
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
