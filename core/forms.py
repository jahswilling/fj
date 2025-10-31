from django import forms
from django.contrib.auth import get_user_model

from accounts.models import *
from .models import *

User = get_user_model()

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("username", 'first_name', 'last_name', "email", "unique_code","phone_no", "account_no", "bank",
                  "signature", "plan1","plan2","plan3","plan4","plan5","pay_date","referrals")

class GuestForm(forms.ModelForm):

    class Meta:
        model = Guest
        fields = ("full_name", "email", "joining", "black_list", "checked_in")
