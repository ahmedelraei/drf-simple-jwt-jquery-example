from django.shortcuts import render
from rest_framework import permissions, serializers, status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, ChangePasswordSerializer, RequestChangePasswordSerializer
from django.views.generic import View
from .models import ChangePasswordRequest
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings


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
        return render(self.request, 'login.html', {})

class RegisterView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'register.html', {})
    

class RequestChangePasswordAPI(UpdateAPIView):
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = RequestChangePasswordSerializer
    model = ChangePasswordRequest

    def get_object(self, queryset=None):
        User = get_user_model()
        obj = User.objects.all()
        return User
            
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.user_model = self.get_object()
            user = self.user_model.objects.get(email=serializer.data.get("email"))

            # Check Email
            if not user.email == serializer.data.get("email"):
                return Response({"email": ["Not found."]}, status=status.HTTP_400_BAD_REQUEST)

            # Set temp. password
            temp_pwd = self.user_model.objects.make_random_password()

            user.set_password(temp_pwd)
            user.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Reset link sent successfully',
            }
            change_pass_url = self.request.build_absolute_uri('/')[:-1] + reverse('change_password')
            msg = f'''
            Commercial Number: {user.commercial_registration_num}\n
            Password: {temp_pwd}\n
            Change password => {change_pass_url}
            '''
            try:
                send_mail(
                    'Login Info',
                    msg,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False
                )
            except Exception as e:
                print(e)


            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)