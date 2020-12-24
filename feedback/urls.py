from django.urls import path

from feedback import views

urlpatterns = [
    path('feedback/', views.FeedbackApi.as_view(), name='feedback'),

]