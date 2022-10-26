import email
from enum import unique
from tabnanny import verbose
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, official_name, address, password = None):
        if not username:
            raise ValueError('Users must have an username')
        if not email:
            raise ValueError('Users must have an email')
        if not official_name:
            raise ValueError('Users must have an officail_name')
        if not address:
            raise ValueError('Users must have an address')
        

        user = self.model(
            username = username,
            email=self.normalize_email(email),
            official_name=official_name,
            address = address,
        )
        #TODO: what about which type of user this is?

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self,username, email, official_name, address, password = None):
        user = self.create_user(
            username = username,
            email=self.normalize_email(email),
            official_name=official_name,
            address = address,
            password = password,
        )

        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    
    email = models.EmailField(verbose_name='email',max_length=60,unique=True)
    username = models.CharField(max_length=30,unique=True)

    ##THESE FIELDS ARE MANDATORY WHEN USING ABSTRACTBASEUSER CLASS
    date_joined = models.DateTimeField(verbose_name='date_joined',auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login',auto_now = True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    #additional fields
    official_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    #last_name = models.CharField(max_length=30)
    is_patient = models.BooleanField(default=False)
    is_hospital = models.BooleanField(default=False)
    is_healthcare_profesional = models.BooleanField(default=False)
    is_pharmacy = models.BooleanField(default=False)
    is_insurance = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    #primary field which will be used for login
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','official_name','address']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True