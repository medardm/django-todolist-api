from django.urls import path
from . import views as todos_views

urlpatterns = [
    path('', todos_views.todo_lists, name='get_todo_lists'),
    path('', todos_views.todo_lists, name='create_todo_list'),
    path('<int:pk>/', todos_views.todo_list_detail, name='todo_list_detail'),
]
