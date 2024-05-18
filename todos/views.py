from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import ScopedRateThrottle

from .models import TodoList, TodoItem
from .serializers import TodoListSerializer, TodoItemSerializer


class TodoListView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'per_minute'

    def get(self, request, format=None):
        todolists = TodoList.objects.filter(user=request.user).prefetch_related('todo_items')
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
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'per_minute'
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


# TODO MOVE THESE IN SEPARATE VIEWS
class TodoItemView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'per_minute'

    def get(self, request, todo_list_pk, format=None):
        request.data.update({"todolist": todo_list_pk})
        todo_items = TodoItem.objects.filter(todolist__id=todo_list_pk, todolist__user=request.user)
        serializer = TodoItemSerializer(todo_items, many=True)
        return Response({'success': 'true', 'message': 'Todo items fetched successfully.', 'data': serializer.data},
                        status=status.HTTP_200_OK)

    def post(self, request, todo_list_pk, format=None):
        request.data.update({"todolist": todo_list_pk})
        serializer = TodoItemSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'true', 'message': 'Todo item created successfully.', 'data': serializer.data},
                            status=status.HTTP_201_CREATED)

        return Response({'success': 'false', 'message': 'Error creating todo item.', 'errors': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


class TodoItemDetailView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'per_minute'

    def get_object(self, todo_list_pk, pk):
        return get_object_or_404(TodoItem, todolist__id=todo_list_pk, id=pk, todolist__user=self.request.user)

    def get(self, request, todo_list_pk, pk, format=None):
        todo_item = self.get_object(todo_list_pk, pk)
        serializer = TodoItemSerializer(todo_item)
        return Response({'success': 'true', 'message': 'Todo item fetched successfully.', 'data': serializer.data})

    def put(self, request, todo_list_pk, pk, format=None):
        todo_item = self.get_object(todo_list_pk, pk)
        serializer = TodoItemSerializer(todo_item, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'true', 'message': 'Todo item updated successfully.', 'data': serializer.data},
                            status=status.HTTP_200_OK)

        return Response({'success': 'false', 'message': 'Error updating todo item.', 'errors': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, todo_list_pk, pk, format=None):
        todo_item = self.get_object(todo_list_pk, pk)
        todo_item.delete()
        return Response({'success': 'true', 'message': 'Todo item was deleted successfully.'},
                        status=status.HTTP_204_NO_CONTENT)
