from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import TodoList, TodoItem
from .serializers import TodoListSerializer, TodoItemsSerializer


@api_view(['GET', 'POST'])
def todo_lists(request, format=None):
    if request.method == 'GET':
        todolists = TodoList.objects.all()
        serializer = TodoListSerializer(todolists, many=True)
        return Response({'success': 'true', 'data': serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = TodoListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'true', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'success': 'false', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def todo_list_detail(request, pk, format=None):
    todo_list = get_object_or_404(TodoList, pk=pk)

    if request.method == 'GET':
        serializer = TodoListSerializer(todo_list)
        return JsonResponse({'success': 'true', 'data': serializer.data}, safe=False)

    elif request.method == 'PUT':
        serializer = TodoListSerializer(todo_list, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'success': 'true', 'data': serializer.data}, safe=False)
        return JsonResponse({'success': 'false', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        todo_list.delete()
        return JsonResponse({'success': 'true', 'message': 'Todo list was deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)
