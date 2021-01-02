from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from login.models import User, StaffProfile


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'unique_id', 'staff_position', 'first_name', 'last_name']
    list_filter = ['staff_position']
    search_fields = ('staff_position',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(StaffProfile)