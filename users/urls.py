from django.urls import path
from .views import RegisterView, UserListView, LoginView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('users', UserListView.as_view()),
]
