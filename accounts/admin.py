from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm,UserAdminChangeForm
# from import_export.admin import ImportExportModelAdmin
# Register your models here.

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.


    fieldsets = (
        (None, {'fields': ()}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'email',"unique_code","phone_no","account_no","bank","signature","referred_by","referrals","plan1","plan2","plan3", "plan4", "plan5","pay_date",'date_joined','password', )}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'is_staff',)}),
    )
    search_fields = ('username',)
    ordering = ('date_joined',)
    filter_horizontal = ()


    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email',"phone_no","account_no","bank","signature","referred_by","referrals","plan1","plan2","plan3","pay_date", 'date_joined', 'password1', 'password2','is_superuser','is_staff', 'is_active')}
        ),
    )

# class userAdminImport(ImportExportModelAdmin,UserAdmin):
#     pass

admin.site.register(CustomUser)
