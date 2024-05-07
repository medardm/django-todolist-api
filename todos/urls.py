from django.urls import path
from . import views as todos_views
from .views import TodoItemView, TodoItemDetailView

urlpatterns = [
    path('', todos_views.TodoListView.as_view()),
    path('<int:pk>/', todos_views.TodoListDetailView.as_view(), name='todo_list_detail'),
    path('<int:todo_list_pk>/todoitems/', TodoItemView.as_view()),
    path('<int:todo_list_pk>/todoitems/<int:pk>/', TodoItemDetailView.as_view()),
]
