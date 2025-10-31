from django.contrib import admin
from .models import * 

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'joining', 'black_list', 'number', 'access_code', 'checked_in', 'is_deleted')
    list_filter = ('joining', 'black_list', 'checked_in', 'is_deleted')
    search_fields = ('full_name', 'email', 'access_code')
    list_editable = ('joining', 'black_list', 'checked_in', 'is_deleted')