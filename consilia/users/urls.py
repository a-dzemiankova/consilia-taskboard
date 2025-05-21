from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUser.as_view(next_page='users:login'), name='login'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
]