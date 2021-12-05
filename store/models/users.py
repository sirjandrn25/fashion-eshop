
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core import validators


class UserManager(BaseUserManager):
    use_in_migrations = True

    # Method to save user to the database
    def save_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        # Call this method for password hashing
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields['is_superuser'] = False
        extra_fields['is_staff'] = False
        return self.save_user(email, password, **extra_fields)

    # Method called while creating a staff user
    def create_staffuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = False
        
        return self.save_user(email, password, **extra_fields) 

    # Method called while calling creatsuperuser
    def create_superuser(self, email, password, **extra_fields):

        # Set is_superuser parameter to true
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser should be True')
        
        extra_fields['is_staff'] = True

        return self.save_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    gender_choices = [
        ('male','Male'),
        ('female','Female')
    ]
    # Primary key of the model
    id = models.BigAutoField(
        primary_key = True,
    )

    full_name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=15,blank=True,null=True,unique=True)
    birth_date = models.DateField(blank=True,null=True)
    avatar = models.ImageField(upload_to="avatar/",blank=True,null=True)
    gender = models.CharField(max_length=10,choices=gender_choices,default=gender_choices[0][0])
    # Email field that serves as the username field
    email = models.CharField(
        max_length = 100, 
        unique = True, 
        validators = [validators.EmailValidator()],
        verbose_name = "Email"
    )

    # Other required fields for authentication
    # If the user is a staff, defaults to false
    is_staff = models.BooleanField(default=False)

    # If the user account is active or not. Defaults to True.
    # If the value is set to false, user will not be allowed to sign in.
    is_active = models.BooleanField(default=True)
    
    # Setting email instead of username
    USERNAME_FIELD = 'email'
    
    # Custom user manager
    objects = UserManager()
    def __str__(self):
        if self.full_name:
            return self.full_name
        return self.email

class Address(models.Model):
    
    provinance_no = models.IntegerField(default=1)
    district = models.CharField(max_length=100,blank=True)
    village = models.CharField(max_length=100,blank=True)
    street = models.CharField(max_length=100,blank=True)
    house_no = models.CharField(max_length=20,blank=True)
    user = models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)

    
    



