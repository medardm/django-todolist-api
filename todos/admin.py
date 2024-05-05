from django.contrib import admin

from . import models

class TodoListAdmin(admin.ModelAdmin):
    list_display = ('user', 'title')


class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('todolist', 'title', 'description', 'completed')


admin.site.register(models.TodoList, TodoListAdmin)
admin.site.register(models.TodoItem, TodoItemAdmin)
