from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):

    def create_user(self,email,username,f_name,l_name,password, **other_fields):

        if not email:
            raise ValueError("You must provide an email address")

        email = self.normalize_email(email)
        user = self.model(email=email,username=username,f_name=f_name,l_name=l_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,username,f_name,l_name,password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(email, username, f_name, l_name, password, **other_fields)


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255)
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    start_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username','f_name','l_name']

    objects = CustomUserManager()

    def __str__(self):
        return(f"{self.email}:{self.username}")