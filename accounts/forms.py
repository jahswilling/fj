
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser
from django.forms.utils import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'password', }),

    )

    password2 = forms.CharField(
        label="Password confirmation",
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'password confirmation', }),

    )

    class Meta():

        model = CustomUser
        fields = ("username", 'first_name', 'last_name', "email", "unique_code","phone_no", "account_no", "bank",
                  "signature", "referred_by", "referrals", "plan1", "plan2", "plan3", "plan4", "plan5","pay_date", "password1", "password2")



class UserChangeForm(forms.ModelForm):

    class Meta():
        fields = ("username", "email", 'first_name', 'last_name',"unique_code","phone_no", "account_no", "bank", "signature", "referred_by", "referrals", "plan1", "plan2", "plan3","plan4", "plan5","pay_date")
        model = CustomUser




class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = (
            'email', 'first_name', 'last_name',
            'username',"unique_code", "phone_no", "account_no", "bank", "signature", "referred_by", "referrals", "plan1", "plan2", "plan3", "plan4", "plan5","pay_date"
        )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = (
            'email', 'first_name', 'last_name',
            'username',"unique_code","phone_no","account_no","bank","signature","referred_by","referrals","plan1","plan2","plan3", "plan4", "plan5","pay_date"
        )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
