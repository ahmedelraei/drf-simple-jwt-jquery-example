from django.shortcuts import render, redirect
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .serializers import UserSerializer, ChangePasswordSerializer
from django.views.generic import View
from accounts.forms import UserLoginForm, UserRegisterForm
from django.contrib.auth import (
    authenticate,
    login,
    logout
)
class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer

class ChangePasswordAPIView(UpdateAPIView):
        serializer_class = ChangePasswordSerializer
        model = get_user_model()

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Invalid password."]}, status=status.HTTP_400_BAD_REQUEST)
                # Set password
                new_pwd = serializer.data.get("new_password")
                confirm_pwd = serializer.data.get("confirm_password")
                if not new_pwd == confirm_pwd:
                    return Response({"Match Error": "Passwords don't match"}, status=status.HTTP_400_BAD_REQUEST)

                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password changed successfully',
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(View):
    def get(self, *args, **kwargs):
        form = UserLoginForm()
        return render(self.request, 'login.html', {'form':form})

class RegisterView(View):
    def get(self, *args, **kwargs):
        form = UserRegisterForm()
        return render(self.request, 'register.html', {'form':form})