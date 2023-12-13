from django.contrib import admin
from .models import Employer, JobPosting, UserCV, GraduateTracer

# Register your models here.
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'address', 'phone_number', 'user_stat']
    # Add more options as needed

class EmployerAdmin(admin.ModelAdmin):
    list_display = ('user_profile','company_name', 'company_address', 'company_email', 'contact_number')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Employer, EmployerAdmin)
admin.site.register(JobPosting)
admin.site.register(UserCV)
admin.site.register(GraduateTracer)
