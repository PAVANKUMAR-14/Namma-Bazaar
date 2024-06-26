from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.

class Account_manager (BaseUserManager):
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email :
            raise ValueError('this is required')
        if not username :
            raise ValueError('this is required')
        
        user=self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self,first_name,last_name,email, username,password):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
         
        user.is_active=True
        user.is_staff=True
        user.is_admin=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user





class Accounts (AbstractBaseUser):
    first_name=models.CharField(max_length=60)
    last_name=models.CharField(max_length=60)
    email=models.EmailField(max_length=60,unique=True)
    username=models.CharField(max_length=60, unique=True)
    phone_number=models.CharField(max_length=50)

    #required
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)


    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name','username']
    objects = Account_manager()

    
    def __str__(self):
        return self.email
    
    def has_perm (self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms (self, add_label):
        return True
    
    def full_name (self):
        return f'{self.first_name} {self.last_name}' 

class UserProfile (models.Model):
    user= models.OneToOneField(Accounts, on_delete=models.CASCADE)
    address_line_1= models.CharField(max_length=100, blank=True)    
    address_line_2= models.CharField( max_length=100, blank=True)
    profile_picture= models.ImageField(upload_to='userprofile',blank=True)
    city= models.CharField(max_length=20)
    state= models.CharField(max_length=20)
    country= models.CharField(max_length=20)

    def __str__(self):
        return self.user.first_name
    
    def full_address (self):
        return f'{self.address_line_1} {self.address_line_2}'

