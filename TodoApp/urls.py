from django.urls import path
from . import views
from .views import RegisterUser, logout_user, LoginUser, about, TaskListView, CreateTaskView

urlpatterns = [
    path('', TaskListView.as_view(), name='home'),
    path('about/', about, name='about'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('addtask/', CreateTaskView.as_view(), name='add_task')
]