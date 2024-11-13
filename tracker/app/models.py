from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from app import enums

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Task(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=enums.StatusChoices.choices, default=enums.StatusChoices.CREATED)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="assigned_tasks",
                                      null=True, blank=True)
    task_completed = models.CharField(max_length=20, choices=enums.CompletedChoices.choices,
                                      default=enums.CompletedChoices.NOT_COMPLETED)
    task_check_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name="checked_tasks",
                                      null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TaskStatusHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='status_history')
    responsible = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.title}:"