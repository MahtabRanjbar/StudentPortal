from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "notes"
        verbose_name_plural = "notes"


class Homework(models.Model):
    subject = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="homework")
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=500)
    due = models.DateTimeField()
    is_finished = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title


class ToDo(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='todo'
        )
    title = models.CharField(max_length=50)
    is_finished = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'ToDo'
        verbose_name_plural = "ToDo"
