from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import TodoList
from .serializers import TodoListSerializer


class TodoListView(APIView):
    """
    List all todo items of authenticated user, create a new todo item, delete a particular todo list, or update a specific todo list.
    """

    def get(self, request, format=None):
        todolists = TodoList.objects.filter(user=request.user)
        serializer = TodoListSerializer(todolists, many=True)
        return Response({'success': 'true', 'message': 'Todo lists fetched successfully.', 'data': serializer.data},
                        status=status.HTTP_200_OK)

    def post(self, request, format=None):
        request.data.update({"user": request.user.id})
        serializer = TodoListSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'true', 'message': 'Todo list created successfully.', 'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response({'success': 'false', 'message': 'Error creating todo list.', 'errors': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


class TodoListDetailView(APIView):
    permission_classes = [IsAuthenticated]
    """
    Retrieve, update or delete a todo item.
    """

    def get_object(self, pk):
        return get_object_or_404(TodoList, pk=pk, user=self.request.user)

    def get(self, request, pk, format=None):
        todo_list = self.get_object(pk)
        serializer = TodoListSerializer(todo_list)
        return Response({'success': 'true', 'message': 'Todo list fetched successfully.', 'data': serializer.data})

    def put(self, request, pk, format=None):
        todo_list = self.get_object(pk)
        serializer = TodoListSerializer(todo_list, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'true', 'message': 'Todo list updated successfully.', 'data': serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({'success': 'false', 'message': 'Error updating todo list.', 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        todo_list = self.get_object(pk)
        todo_list.delete()

        return Response({'success': 'true', 'message': 'Todo list was deleted successfully.'},
                        status=status.HTTP_204_NO_CONTENT)
