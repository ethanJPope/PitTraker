from django.db import models
from django.contrib.auth.models import AbstractUser


class TodoItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)  # Add this line
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


class LoanedTool(models.Model):
    team_number = models.CharField(max_length=10)
    tool_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_loaned = models.DateTimeField(auto_now_add=True)
    returned = models.BooleanField(default=False)
    date_returned = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Team {self.team_number} - {self.tool_name}"

    class Meta:
        ordering = ["-date_loaned"]
