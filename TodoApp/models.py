from django.db import models

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

    PRIORITY_CHOICES = [
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low'),
    ]

    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")

    priority = models.IntegerField(
        choices=PRIORITY_CHOICES,
        default=MEDIUM,
        verbose_name='Приоритет'
    )

    deadline = models.DateTimeField(null=True, blank=True, verbose_name="Дедлайн")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
    )

    is_done = models.BooleanField(default=False, verbose_name="Решена")

    def __str__(self):
        return self.title

    def is_overdue(self):
        return self.deadline and self.deadline < timezone.now()

    class Meta:
        ordering = ('priority', 'deadline')
        verbose_name = 'Задачи'
        verbose_name_plural = 'Задачи'