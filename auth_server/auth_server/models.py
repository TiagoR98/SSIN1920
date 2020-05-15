from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class AuthorizationCode(models.Model):
    code = models.CharField(max_length=50)
    client_id = models.CharField(max_length=50)
    scope = models.CharField(max_length=50)
    redirect_uri = models.CharField(max_length=100)
    expiration =  models.DateTimeField()

    def __str__(self):
        return self.code
