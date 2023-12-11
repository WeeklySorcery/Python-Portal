from django.contrib import admin

# Register your models here.
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'address', 'phone_number', 'user_stat']
    # Add more options as needed

admin.site.register(UserProfile, UserProfileAdmin)