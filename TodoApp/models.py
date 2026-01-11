from django.db import models

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Task(models.Model):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

    PRIORITY_CHOICES = [
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low'),
    ]

    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
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

    def get_absolute_url(self):
        return reverse('task', kwargs={'task_slug': self.slug})

    def is_overdue(self):
        return self.deadline and self.deadline < timezone.now()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

            unique_slug = self.slug
            counter = 1

            while Task.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{self.slug}-{counter}"
                counter += 1
            self.slug = unique_slug

        super().save(*args, **kwargs)

    class Meta:
        ordering = ('priority', 'deadline')
        verbose_name = 'Задачи'
        verbose_name_plural = 'Задачи'