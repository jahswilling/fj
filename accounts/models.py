import uuid
import os

from django.db import models
from django.contrib.auth.models import AbstractUser


def image_file_path(instance, filename):
    """Generate file path for new profile image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/profilePic/', filename)


class CustomUser(AbstractUser):
    unique_code = models.CharField(max_length=200,)
    account_no = models.CharField(max_length=200,)
    bank = models.CharField(max_length=200,)
    phone_no   = models.CharField(max_length=200,)
    signature = models.FileField(
        upload_to=image_file_path, default='', blank=True, null=True)
    referred_by   = models.CharField(max_length=200,blank=True, null=True)
    referrals   = models.TextField(blank=True, null=True)
    plan1   = models.CharField(max_length=20000,blank=True, null=True)
    plan2   = models.CharField(max_length=20000,blank=True, null=True)
    plan3   = models.CharField(max_length=20000,blank=True, null=True)
    plan4   = models.CharField(max_length=20000,blank=True, null=True)
    plan5   = models.CharField(max_length=20000,blank=True, null=True)
    pay_date   = models.CharField(max_length=20000,blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
