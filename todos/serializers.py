from rest_framework import serializers

from todos.models import TodoList, TodoItem


class TodoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoList
        fields = '__all__'


class TodoItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = '__all__'
