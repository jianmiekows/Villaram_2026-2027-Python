from django.urls import path

from .views import UserDetailView, UserListCreateView

app_name = 'clients'

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
