from django.urls import path
from .views import RegisterView, UserListView, LoginView, LogoutView, ValidateTokenView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('users', UserListView.as_view()),
    path('token/validate', ValidateTokenView.as_view()),
]
