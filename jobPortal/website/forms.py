from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Employer, JobPosting, UserCV, GraduateTracer


class CreateUserForm(UserCreationForm):

    email = forms.EmailField(required=True, error_messages={'required': 'email required.'})
    first_name = forms.CharField(max_length=30, error_messages={'required': 'first name required.'})
    last_name = forms.CharField(max_length=30, error_messages={'required': 'last name required.'})
    user_stat = forms.ChoiceField(choices=[('jobSeeker', 'Job Seeker'), ('employer', 'Employer')])
    password1 = forms.CharField(widget=forms.PasswordInput, required=True, error_messages={'required': 'Please enter a password.'})
    password2 = forms.CharField(widget=forms.PasswordInput, required=True, error_messages={'required': 'Please re-enter your password.'})

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'user_stat']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use. Please use a different email.')
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('The passwords do not match. Please enter the same password in both fields.')
        return password2

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic','phone_number', 'address', 'gender', 'skill_description']
        # Add other fields as needed

class EmployerEditForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['company_name','company_address', 'company_email', 'contact_number', 'company_logo', 'company_desc']
        # Add other fields as needed

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['job_title','job_description', 'job_requirements', 'job_location', 'salary', 'application_deadline', 'job_type']
        # Add other fields as needed

class UserCVForm(forms.ModelForm):
    class Meta:
        model = UserCV
        fields = ['resume']

class GraduateTracerForm(forms.ModelForm):
    class Meta:
        model = GraduateTracer
        exclude = ['user']  # Exclude the 'user' field from the form, as it will be set in the view