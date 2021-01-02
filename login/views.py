from django.contrib.auth import login, get_user_model
# from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics, status
# Create your views here.
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from login.models import StaffProfile
from login.serializers import RegisterSerializer, UserSerializer, ChangePasswordSerializer, UpdateUserSerializer, \
    LogoutSerializer, UserProfileSerializer, UpdateUserProfileSerializer

User = get_user_model()


# user registration view
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# user list view
class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer


# user detail view
class UserDetail(generics.RetrieveAPIView):
    queryset = StaffProfile.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer


# change password view
class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


# update user
class UpdateUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer


# user profile view
class UserProfileView(generics.CreateAPIView):
    queryset = StaffProfile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer


# update user profile

class UpdateUserProfileView(generics.UpdateAPIView):
    queryset = StaffProfile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserProfileSerializer

# logout view
class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token)

        return Response(status=status.HTTP_205_RESET_CONTENT)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDelete(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


"""
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'message': 'User Created Successfully. Now perform Login to get your token'
        })
"""
