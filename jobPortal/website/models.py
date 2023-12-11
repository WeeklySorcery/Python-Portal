from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    user_stat = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Employer(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='employer')
    company_name = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255)
    company_email = models.EmailField()
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user_profile.user.username