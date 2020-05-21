from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime, timedelta

class MyAccountManager(BaseUserManager):
	def create_user(self, username, password=None):
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, password):
		user = self.create_user(
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Client(AbstractBaseUser):
	username 				= models.CharField(max_length=50, unique=True)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)


	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []

	objects = MyAccountManager()

	def __str__(self):
		return self.username

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True

class AuthorizationCode(models.Model):
    code = models.CharField(max_length=50)
    client_id = models.CharField(max_length=50)
    scope = models.CharField(max_length=50)
    redirect_uri = models.CharField(max_length=100)
    expiration =  models.DateTimeField()

    def __str__(self):
        return self.code

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username

def getExpiration():
   return datetime.now() + timedelta(minutes=15)

class Token(models.Model):
	access = models.CharField(max_length=250, unique=True)
	refresh = models.CharField(max_length=250, unique=True)
	client = models.ForeignKey(Client, on_delete=models.CASCADE)
	scope = models.CharField(max_length=50)
	expiration =  models.DateTimeField(default=getExpiration)

	def __str__(self):
		return self.access
