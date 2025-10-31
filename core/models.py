from django.db import models
from django.conf import settings
import json

class Activities(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Guest(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, blank=True, null=True, help_text="Email address for sending invites")
    joining = models.CharField(max_length=3, choices=(('Yes', 'Yes'), ('No', 'No')), default='No')
    black_list = models.BooleanField(default=False)
    number = models.IntegerField(default=1)
    access_code = models.CharField(max_length=10, blank=True, unique=True)
    checked_in = models.BooleanField(default=False)
    invite_sent = models.BooleanField(default=False, help_text="Has this guest already been sent an invite?")
    image = models.TextField(null=True, blank=True)
    qr_code = models.TextField(null=True, blank=True, help_text="Base64 encoded QR code image")
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        creating = not self.pk
        if creating:
            # Only auto-assign if not specified (allow data migration for old records)
            last_number = Guest.objects.aggregate(models.Max('number')).get('number__max')
            self.number = (last_number or 0) + 1
            self.access_code = f'fj25{self.number:03d}'
        super().save(*args, **kwargs)
