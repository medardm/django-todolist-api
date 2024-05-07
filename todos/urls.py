from django.urls import path
from . import views as todos_views

urlpatterns = [
    path('', todos_views.TodoListView.as_view()),
    path('<int:pk>/', todos_views.TodoListDetailView.as_view(), name='todo_list_detail'),
]
