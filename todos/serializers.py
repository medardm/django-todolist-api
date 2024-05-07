from rest_framework import serializers

from todos.models import TodoList, TodoItem


class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = '__all__'


class TodoListSerializer(serializers.ModelSerializer):
    todo_items = TodoItemSerializer(many=True, read_only=True)

    class Meta:
        model = TodoList
        fields = '__all__'
