from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import TodoList, TodoItem
from .serializers import TodoListSerializer, TodoItemsSerializer


class TodoListView(APIView):
    """
    List all todo items, or create a new todo item.
    """

    def get(self, request, format=None):
        todolists = TodoList.objects.all()
        serializer = TodoListSerializer(todolists, many=True)
        return Response({'success': 'true', 'message': 'Todo lists fetched successfully.', 'data': serializer.data},
                        status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = TodoListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'true', 'message': 'Todo list created successfully.', 'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response({'success': 'false', 'message': 'Error creating todo list.', 'errors': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


class TodoListDetailView(APIView):
    """
    Retrieve, update or delete a todo item.
    """

    def get_object(self, pk):
        return get_object_or_404(TodoList, pk=pk)

    def get(self, request, pk, format=None):
        todo_list = self.get_object(pk)
        serializer = TodoListSerializer(todo_list)
        return Response({'success': 'true', 'message': 'Todo list fetched successfully.', 'data': serializer.data})

    def put(self, request, pk, format=None):
        todo_list = self.get_object(pk)
        serializer = TodoListSerializer(todo_list, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'true', 'message': 'Todo list updated successfully.', 'data': serializer.data})
        return Response({'success': 'false', 'message': 'Error updating todo list.', 'errors': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        todo_list = self.get_object(pk)
        todo_list.delete()
        return Response({'success': 'true', 'message': 'Todo list was deleted successfully!'},
                        status=status.HTTP_204_NO_CONTENT)
