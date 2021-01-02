from django.urls import path

from login import views
from login.views import LogoutView, LogoutAllView, LogoutAPIView

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('list_users/', views.UserView.as_view(), name='list_user'),
    path('user_details/<int:pk>/', views.UserDetail.as_view(), name='user_details'),
    path('change_password/<int:pk>/', views.ChangePasswordView.as_view(), name='change_password'),
    path('user_profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('update_user/<int:pk>/', views.UpdateUserView.as_view(), name='update_profile'),
    path('update_user_profile/<int:pk>/', views.UpdateUserProfileView.as_view(), name='update_user_profile'),
    path('delete_user/<int:pk>/', views.UserDelete.as_view(), name='delete_user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout_all/', LogoutAllView.as_view(), name='logout_all'),
]