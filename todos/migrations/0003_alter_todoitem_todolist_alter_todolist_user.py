# Generated by Django 4.2.11 on 2024-05-06 15:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todos', '0002_todoitem_created_todoitem_updated_todolist_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoitem',
            name='todolist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todo_items', to='todos.todolist'),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todo_lists', to=settings.AUTH_USER_MODEL),
        ),
    ]