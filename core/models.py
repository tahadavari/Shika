import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone


# Create your models here.
class BaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

    def archive(self):
        return super().get_queryset()


class BaseModel(models.Model):
    deleted = models.BooleanField(default=False)
    delete_timestamp = models.DateTimeField(null=True, blank=True)
    creat_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    objects = BaseManager()

    class Meta:
        abstract = True


class User(AbstractUser):
    pass
