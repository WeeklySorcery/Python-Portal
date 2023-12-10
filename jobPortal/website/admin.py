from django.contrib import admin

# Register your models here.
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['profile_pic','user', 'gender', 'address', 'phone_number', 'status']
    # Add more options as needed

admin.site.register(UserProfile, UserProfileAdmin)