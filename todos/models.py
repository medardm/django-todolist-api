from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class TodoList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='todo_lists')
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'title',)

    def __str__(self):
        return self.title


class TodoItem(models.Model):
    todolist = models.ForeignKey(TodoList,
                                 on_delete=models.CASCADE,
                                 related_name='todo_items')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('todolist', 'title',)

    def __str__(self):
        return self.title
