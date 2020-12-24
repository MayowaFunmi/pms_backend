from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from feedback.models import Feedback
from feedback.serializers import FeedbackSerializer


class FeedbackApi(generics.CreateAPIView):
    queryset = Feedback.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = FeedbackSerializer
