from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


class CustomUserManager(BaseUserManager):
    """Manager For User Profiles"""

    def create_user(self, email, commercial_num, password=None):
        """Create a new user profile """
        if not email:
            raise ValueError('User Must Have an Email Address')
        email = self.normalize_email(email)
        user = self.model(email=email, commercial_registration_num=commercial_num)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, commercial_registration_num, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, commercial_registration_num, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """ Database model For Users in the System"""
    email = models.EmailField(max_length=255, unique=True)
    #user_type = models.CharField(max_length=20, choices=USER_TYPES)
    commercial_registration_num = models.CharField(max_length=50, unique=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'commercial_registration_num'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = "User"

    def __str__(self):
        """Return String Representation of our user """
        return self.email
        

class ChangePasswordRequest(models.Model):
    email = models.CharField(max_length=50)
    otp = models.CharField(max_length=5)

""" TODO:
1- make registration for the model user and send link for the user email to change password 
2- redirect user to change password api with the following:
	- old password
	- new password
	- confirm password
3- make login
4- make request change password with email
- its prefable user djangorestframework-simplejwt for authentication """