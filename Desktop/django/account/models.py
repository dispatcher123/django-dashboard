from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


GENDER=(
    ('MALE','MALE'),
    ('FEMALE','FEMALE'),
)
STATUS=(
    ('STUDENTS','STUDENTS'),
    ('JUNIOR','JUNIOR'),
    ('MID','MID'),
    ('SENIOR','SENIOR')
)
class User(AbstractBaseUser):
    email=models.EmailField(max_length=200,unique=True)
    username=models.CharField(max_length=200,unique=True)
    first_name=models.CharField(max_length=250)
    last_name=models.CharField(max_length=250)
    phone_number=models.CharField(max_length=250)
    gender=models.CharField(max_length=250,choices=GENDER)
    status=models.CharField(max_length=250,choices=STATUS)
    
    
    is_active=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)
    login_date=models.DateTimeField(auto_now_add=True) # it would be joined_date
    joined_date=models.DateTimeField(auto_now=True)
    
    objects=MyAccountManager()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=('username','first_name','last_name')
    
    def __str__(self):
        return self.email
    
    def has_perm(self,obj=None):
        return self.is_admin
        
    def has_module_perms(self,add_label):
        return True