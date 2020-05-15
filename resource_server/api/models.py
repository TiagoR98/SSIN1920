from django.db import models

# Create your models here.

class Resource(models.Model):
    """
    Resource instance model.

    Model used to represent an resource.
    """
    data = models.TextField()
