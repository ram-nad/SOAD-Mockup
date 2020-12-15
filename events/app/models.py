from django.db import models
import uuid


# Create your models here.
class Session(models.Model):
    session = models.CharField(max_length=80, auto_created=True, default=uuid.uuid4, unique=True)
    access = models.CharField(max_length=50)
