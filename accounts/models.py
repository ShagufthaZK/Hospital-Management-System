
import email
from email.policy import default
from enum import unique
from random import choices
from tabnanny import verbose
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

USER_TYPE = [('patient','Patient'),('hospital','Hospital'),('pharmacy','Pharmacy'),('insurance','Insurance Company'),('professional','Healthcare Professional')]

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, official_name, address, user_type, mobile, password = None):
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
            user_type = user_type,
            mobile = mobile,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self,username, email, official_name, address, user_type,mobile, password = None):
        user = self.create_user(
            username = username,
            email=self.normalize_email(email),
            official_name=official_name,
            address = address,
            user_type = user_type,
            mobile = mobile,
            password = password,
        )

        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.is_approved = True
        user.is_email_verified = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    
    email = models.EmailField(verbose_name='email',max_length=60,unique=True)
    is_email_verified = models.BooleanField(default=False)
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
    mobile = models.IntegerField(default=0)
    is_approved = models.BooleanField(default=False)
    user_type = models.CharField(max_length=30,choices=USER_TYPE)

    #primary field which will be used for login
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','official_name','address','user_type','mobile']

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


class OTPMobileVerification(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True)
    otp = models.CharField(max_length=6)
    generated_at = models.DateTimeField(auto_now = True)
    valid_till = models.IntegerField(default=60)#otp is valid till 60s after generated_at timestamp

class UserFiles(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    file_name = models.CharField(max_length=30,blank=True)
    file = models.FileField(upload_to="users/files/")

    def delete(self, *args,**kwargs):
        self.file.delete()
        super().delete(*args,**kwargs)

class SharedFiles(models.Model):
    file = models.ForeignKey(UserFiles,on_delete=models.CASCADE)
    shared_to = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
