from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, tc_kimlik_no, email, password=None, **extra_fields):
        if not tc_kimlik_no:
            raise ValueError('TC Kimlik No gereklidir.')
        if not email:
            raise ValueError('Email adresi gereklidir.')

        email = self.normalize_email(email)
        user = self.model(tc_kimlik_no=tc_kimlik_no, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, tc_kimlik_no, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(tc_kimlik_no, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('aday', 'Aday'),
        ('admin', 'Admin'),
        ('yonetici', 'Yönetici'),
        ('juri', 'Jüri'),
    ]

    id = models.AutoField(primary_key=True)
    tc_kimlik_no = models.CharField(max_length=11, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField()

    USERNAME_FIELD = 'tc_kimlik_no'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'role']

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

    class Meta:
        managed = False
        db_table = 'users'
