from django.urls import path

from login import views
from login.views import LogoutView, LogoutAllView, LogoutAPIView

urlpatterns = [
    path('register/', views.RegisterApi.as_view(), name='register'),
    path('list_users/', views.UserView.as_view(), name='list_user'),
    path('change_password/<int:pk>/', views.ChangePasswordView.as_view(), name='change_password'),
    path('update_profile/<int:pk>/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('delete_user/<int:pk>/', views.UserDelete.as_view(), name='delete_user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout_all/', LogoutAllView.as_view(), name='logout_all'),
]