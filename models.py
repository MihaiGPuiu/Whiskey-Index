from django.db import models

# Create your models here.
class TodoItem(models.Model):
    title=models.CharField(max_length=200)
    completed=models.BooleanField(default=False)
class Whiskey(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    # Add other fields as needed

    def __str__(self):
        return self.name