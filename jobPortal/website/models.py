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
    skill_description = models.TextField(null=True, blank=True)


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
    
class GraduateTracer(models.Model):
    COLLEGE_DEPARTMENT_CHOICES = [
        ('', 'Choose'),
        ('College of Information and Communication Technology (CICT)', 'College of Information and Communication Technology (CICT)'),
        ('College of Business Administration (CBA)', 'College of Business Administration (CBA)'),
        ('College of Architecture and Fine Arts (CAFA)', 'College of Architecture and Fine Arts (CAFA)'),
        ('College of Arts and Letters (CAL)', 'College of Arts and Letters (CAL)'),
        ('College of Criminal Justice Education (CCJE)', 'College of Criminal Justice Education (CCJE)'),
        ('College of Social Science and Philosophy (CSSP)', 'College of Social Science and Philosophy (CSSP)'),
        ('College of Home Economics (CHE)', 'College of Home Economics (CHE)'),
        ('College of Industrial Technology (CIT)', 'College of Industrial Technology (CIT)'),
        ('College of Nursing (CON)', 'College of Nursing (CON)'),
        ('College of Engineering (COE)', 'College of Engineering (COE)'),
        ('College of Education (COED)', 'College of Education (COED)'),
        ('College of Sports, Exercise and Recreation', 'College of Sports, Exercise and Recreation'),
        ('College of Science (CS)', 'College of Science (CS)'),
    ]

    YEAR_CHOICES = [
        ('', 'Select Year'),
        ('2010', '2010'),
        ('2011', '2011'),
        ('2012', '2012'),
        ('2013', '2013'),
        ('2014', '2014'),
        ('2015', '2015'),
        ('2016', '2016'),
        ('2017', '2017'),
        ('2018', '2018'),
        ('2019', '2019'),
        ('2020', '2020'),
        ('2021', '2021'),
        ('2022', '2022'),
        ('2023', '2023'),
        ('2024', '2024'),
    ]

    CIVIL_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Separated', 'Separated'),
        ('Widowed', 'Widowed'),
        ('Other', 'Other'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    AGE_CHOICES = [
        ('', 'Select Age'),
        ('Below 20', 'Below 20'),
        ('20-25', '20-25'),
        ('26-30', '26-30'),
        ('31-35', '31-35'),
        ('36-40', '36-40'),
        ('Above 40', 'Above 40'),
        ('Other', 'Other'),
    ]

    EDUCATION_LEVEL_CHOICES = [
        ('', 'Select'),
        ('Certificate in Two Year Course', 'Certificate in Two Year Course'),
        ('College Graduate', 'College Graduate'),
        ('with Units in Masters Degree', 'with Units in Masters Degree'),
        ('Masters Degree Holder', 'Masters Degree Holder'),
        ('with Doctoral Degree', 'with Doctoral Degree'),
        ('Doctoral Degree Holder', 'Doctoral Degree Holder'),
    ]

    SCHOLARSHIP_CHOICES = [
        ('', 'Select'),
        ('Yes, I am a recipient of a GOVERTNMENT scholarship program', 'Yes, I am a recipient of a GOVERTNMENT scholarship program'),
        ('Yes, I am recipient of a PRIVATE scholarship program', 'Yes, I am recipient of a PRIVATE scholarship program'),
        ('No, I am not a recipient of ANY scholarship program', 'No, I am not a recipient of ANY scholarship program'),
    ]

    EMPLOYMENT_CHOICES = [
        ('', 'Select'),
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Never', 'Never'),
    ]

    EMPLOYMENT_STATUS_CHOICES = [
        ('', 'Select'),
        ('Regular/Permanent', 'Regular/Permanent'),
        ('Contractual', 'Contractual'),
        ('Temporary', 'Temporary'),
        ('Self-Employed', 'Self-Employed'),
    ]

    LINE_OF_BUSINESS_CHOICES = [
        ('', 'Select'),
        ('Agriculture', 'Agriculture'),
        ('Hunting and Forestry', 'Hunting and Forestry'),
        ('Fishing', 'Fishing'),
        ('Mining', 'Mining'),
        ('Construction', 'Construction'),
        ('Manufacturing', 'Manufacturing'),
        ('Transportation', 'Transportation'),
        ('Communication', 'Communication'),
        ('Finance', 'Finance'),
        ('Real Estate', 'Real Estate'),
        ('Education', 'Education'),
        ('Healthcare', 'Healthcare'),
        ('Technology', 'Technology'),
        ('Retail', 'Retail'),
        ('Hospitality', 'Hospitality'),
        ('Arts and Entertainment', 'Arts and Entertainment'),
        ('Other', 'Other'),
    ]

    WORK_PLACE_CHOICES = [
        ('', 'Select'),
        ('Local', 'Local'),
        ('Abroad', 'Abroad'),
    ]

    FIRST_JOB_CHOICES = [
        ('', 'Select'),
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    FIRST_JOB_RELATED_CHOICES = [
        ('', 'Select'),
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    FIRST_JOB_DURATION_CHOICES = [
        ('', 'Select'),
        ('less than a month', 'Less than a month'),
        ('1 to 6 months', '1 to 6 months'),
        ('7 to 11 months', '7 to 11 months'),
        ('1 year to less than 2 years', '1 year to less than 2 years'),
        ('2 years to less than 3 years', '2 years to less than 3 years'),
        ('3 years to less than 4 years', '3 years to less than 4 years'),
        ('Other', 'Other'),
    ]

    FIRST_JOB_LAND_DURATION_CHOICES = [
        ('', 'Select'),
        ('less than a month', 'Less than a month'),
        ('1 to 6 months', '1 to 6 months'),
        ('7 to 11 months', '7 to 11 months'),
        ('1 year to less than 2 years', '1 year to less than 2 years'),
        ('2 years to less than 3 years', '2 years to less than 3 years'),
        ('3 years to less than 4 years', '3 years to less than 4 years'),
        ('Other', 'Other'),
    ]

    MONTHLY_EARNING_CHOICES = [
        ('', 'Select'),
        ('Below ₱5,000,00', 'Below ₱5,000,00'),
        ('₱5,000,00 to less than ₱10,000,00', '₱5,000,00 to less than ₱10,000,00'),
        ('₱10,000,00 to ₱15,000,00', '₱10,000,00 to ₱15,000,00'),
        ('₱15,000,00 to ₱20,000,00', '₱15,000,00 to ₱20,000,00'),
        ('₱20,000,00 to ₱25,000,00', '₱20,000,00 to ₱25,000,00'),
        ('₱25,000,00 to ₱30,000,00', '₱25,000,00 to ₱30,000,00'),
        ('Other', 'Other'),
    ]

    CURRICULUM_RELEVANCE_CHOICES = [
        ('', 'Select'),
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    # Reference the Signup model using a ForeignKey
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college_department = models.CharField(max_length=255, choices=COLLEGE_DEPARTMENT_CHOICES, default='',)
    course = models.CharField(max_length=255, blank=True, null=True)
    year_graduated = models.CharField(max_length=4, choices=YEAR_CHOICES, default='',)
    fullname = models.CharField(max_length=255, blank=True, null=True)
    civil_status = models.CharField(max_length=10, choices=CIVIL_STATUS_CHOICES, default='Other')
    age = models.CharField( max_length=10, choices=AGE_CHOICES, default='')
    address = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Other')
    email = models.EmailField(blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    education_level = models.CharField(max_length=50, choices=EDUCATION_LEVEL_CHOICES, default='')
    scholarship = models.CharField(max_length=100, choices=SCHOLARSHIP_CHOICES, default='')
    presently_employed = models.CharField(max_length=10, choices=EMPLOYMENT_CHOICES, default='')
    unemployment_reason = models.TextField(max_length=200, blank=True, null=True)
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS_CHOICES, default='')
    occupation = models.CharField(max_length=255, blank=True, null=True)
    line_of_business = models.CharField(max_length=200, choices=LINE_OF_BUSINESS_CHOICES, default='')
    work_place = models.CharField(max_length=10, choices=WORK_PLACE_CHOICES, default='')
    firstjob_after_college = models.CharField(max_length=3, choices=FIRST_JOB_CHOICES, default='')
    reasons_for_staying = models.TextField(max_length=200, blank=True, null=True)
    firstjob_related = models.CharField(max_length=3, choices=FIRST_JOB_RELATED_CHOICES, default='')
    reason_for_accepting = models.TextField(max_length=200, blank=True, null=True)
    reason_for_changing = models.TextField(max_length=200, blank=True, null=True)
    firstjob_duration = models.CharField(max_length=30, choices=FIRST_JOB_DURATION_CHOICES, default='')
    find_your_firstjob = models.TextField(max_length=200, blank=True, null=True)
    firstjob_land_duration = models.CharField(max_length=30, choices=FIRST_JOB_LAND_DURATION_CHOICES, default='')
    where_you_find_firstjob = models.TextField(max_length=200, blank=True, null=True)
    monthly_earning = models.CharField(max_length=200, choices=MONTHLY_EARNING_CHOICES, default='')
    curriculum_relevance_firstjob = models.CharField(max_length=5, choices=CURRICULUM_RELEVANCE_CHOICES, default='')
    competencies_usefull_firstjob = models.TextField(max_length=200, blank=True, null=True)

# Messages

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender} to {self.recipient}: {self.content}'

    class Meta:
        ordering = ('timestamp',)