from django.db import models
from django.contrib.auth.models import User
import uuid

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
    company_logo = models.ImageField(upload_to='company_logo/', null=True, blank=True)
    company_desc = models.CharField(max_length=655, null=True, blank=True)
    

    def __str__(self):
        return self.user_profile.user.username
    
class JobPosting(models.Model):
    JOB_TYPE_CHOICES = [
    ('full_time', 'Full Time'),
    ('freelancer', 'Freelancer'),
    ('part_time', 'Part Time'),
    ('intern', 'Intern'),
    ]
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='job_postings')
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    job_requirements = models.TextField()
    job_location = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    application_deadline = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.job_title} at {self.employer.company_name}"
    
    @property
    def num_applicants(self):
        return UserCV.objects.filter(job_posting=self).count()

    
class UserCV(models.Model):
    resume = models.FileField(upload_to='user_cvs/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    company = models.CharField(max_length=255)

    def __str__(self):
        return f"CV for {self.user.username} - {self.job_posting.job_title} at {self.company}"