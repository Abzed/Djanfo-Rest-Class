from statistics import mode
import uuid
from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

GENDER = (
    ('Male','MALE'),
    ('Female','FEMALE'),
    ('Other','OTHER'),
)

TYPES =(    
    ('Devops', 'DEVOPS'),
    ('Fullstack', 'FULLSTACK'), 
    ('Frontend', 'FRONTEND'),
    ('Backend', 'BACKEND'),
    ('Cloud', 'CLOUD')
)

class SystemUserAccountManager(BaseUserManager):
    def create_user(self,username, email, first_name, last_name, password=None):
        if not username and email:
            raise ValueError('Email and username must be set!')
        user = self.model(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,username, email, first_name, last_name, password):
        user = self.create_user(username, email, first_name, last_name, password)
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save()
        return user
    
    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return  self.email

    def has_perm(self, perm, ob=None):
        return True

    def has_module_perms(self, app_label):
        return True




class SystemUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=19, null = True, blank = True, unique=True)    
    phone_number = models.IntegerField(null = True, blank = True)
    avatar = CloudinaryField('image', folder="student_management")
    gender = models.CharField(choices=GENDER, max_length=55, null=True, blank=True)
    first_name = models.CharField(_('first name'), max_length=40)
    last_name = models.CharField(_('last name'), max_length=50)
    email = models.EmailField(_('email address'), unique=True) 
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    
    ordering = ('username',)
    list_display = ('first_name', 'last_name', 'email', 'gender')
    
    USERNAME_FIELD = 'username'
    
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
    
    objects = SystemUserAccountManager()
    
    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return  self.email

    def has_perm(self, perm, ob=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def natural_key(self):
        return self.email

class Student(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.OneToOneField(SystemUser, on_delete=models.CASCADE, related_name='student_profile')
    location = models.CharField(max_length=55)
    joined_on = models.DateTimeField(auto_now_add=True)
    stack = models.CharField(choices=TYPES, max_length=55)
    payment = models.IntegerField(null = True, blank = True, default=0)
    
    def __str__(self):
        return self.account.username
    
class Mentor(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.OneToOneField(SystemUser, on_delete=models.CASCADE, related_name='mentor_profile')
    stack = models.CharField(choices=TYPES, max_length=55)
    
    def __str__(self):
        return self.account.username
    
class Classroom(models.Model):
    class_name = models.CharField(max_length=50, null=True, blank=True)
    student = models.ManyToManyField(Student, blank=True)
    instructor = models.ForeignKey(Mentor, blank=True, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.class_name
    
    
        