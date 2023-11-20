from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, dob, mobile, password, role, otp=None, reset_token=None, created_at=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, dob=dob, mobile=mobile, role=role, otp=otp, reset_token=reset_token, created_at=created_at, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, dob, mobile, password=None, role=None, otp=None, reset_token=None, created_at=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, dob, mobile, password, role, otp, reset_token, created_at, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255,blank=False)
    dob = models.DateField(blank=False)
    mobile = models.CharField(max_length=15, unique=True,blank=False)
    email = models.EmailField(unique=True,blank=False)
    password = models.CharField(max_length=128,blank=False)
    role = models.CharField(max_length=255, blank=False)
    otp = models.CharField(max_length=255, blank=True,null=True)
    reset_token = models.CharField(max_length=128, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'dob', 'mobile','role']

    def __str__(self):
        return self.email
