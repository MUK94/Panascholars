from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist

from core.abstract.models import AbstractManager, AbstractModel

from django.http import Http404

    
class UserManager(BaseUserManager, AbstractManager):
    def get_object_by_public_id(self, public_id):
        try:
            instance = self.get(public_id=public_id)
            return instance
        except(ObjectDoesNotExist, ValueError, TypeError):
            return Http404
        
    # Create User
    def create_user(self, username, email, password=None, **kwargs):
        
        # Create and return a user with specied fields
        if username is None:
            raise TypeError('Username is required.')
        if email is None:
            raise TypeError('Email is required.')
        if password is None:
            raise TypeError('Password is required.')
        
        user = self.model(username=username, email=self.normalize_email(email), **kwargs ) 
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    # Create superuser
    def create_superuser(self, username, email, password, **kwargs):
        
        # Create and return a superuser (admin)
        if email is None:
            raise TypeError('Email is required')
        if username is None:
            raise TypeError('Username is required')
        if password is None:
            raise TypeError('Password is required')
        
        user = self.create_user(username, email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        
        return user
        
class User(AbstractModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True)
    
     
    USERNAME_FIELD = 'email' # Unique field for authentication
    REQUIRED_FIELDS = ['username'] # Required when creating a user 
    
    objects = UserManager()
    
    def __str__(self):
        return f"{self.email}"
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    