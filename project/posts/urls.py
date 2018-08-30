from django.urls import path

from . import views, schedulers

app_name = 'posts'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('generate/', schedulers.GenerateRandomUserView.as_view(), name='generate_posts'),
    path('users_list/', schedulers.UserListView.as_view(), name='users_list')
]