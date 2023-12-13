from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CreateUserForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from .forms import UserProfileEditForm, EmployerEditForm, JobPostingForm  
from django.views import View
from django.db import IntegrityError
from .models import UserProfile, Employer, JobPosting
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def about(request):
    return render(request, 'about.html', {})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            # Redirect to home or any other desired page
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Set the username to the user's email
            user.username = user.email
            
            # Save the user
            user.save()

            # Determine the group based on the selected option in the form
            user_group = form.cleaned_data['user_stat']
            
            # Get or create the group
            group, created = Group.objects.get_or_create(name=user_group)
            
            # Add the user to the group
            group.user_set.add(user)

            # Create UserProfile
            user_profile = UserProfile.objects.create(user=user, user_stat=user_group)

            # Create Employer if the user is an employer
            if user_group == 'employer':
                employer = Employer.objects.create(user_profile=user_profile, company_name="Default Name", company_address="Default Address", company_email="default@example.com", contact_number="123456789")
                
            # Log the user in
            auth_login(request, user)

            return redirect('home')  # Redirect to home or any other desired page
    else:
        form = CreateUserForm()

    return render(request, 'signup.html', {'form': form})

def user_logout(request):
    # Log the user out
    logout(request)
    # Redirect to the home page or any other desired page
    return redirect('home')

@login_required
def profile(request, username):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=username)  # Redirect to the profile page after saving
    else:
        form = UserProfileEditForm(instance=user_profile)

    return render(request, 'profile.html', {'form': form})

@login_required
def company_profile(request):
    try:
        # Assuming the user is logged in and there is a corresponding Employer profile
        employer = Employer.objects.get(user_profile__user=request.user)
    except Employer.DoesNotExist:
        # Handle the case where the Employer profile doesn't exist
        employer = None

    if request.method == 'POST':
        # Handle form submission
        form = EmployerEditForm(request.POST, request.FILES, instance=employer)
        if form.is_valid():
            form.save()
            # Redirect to the same view or another page after successful form submission
            return redirect('company_profile')
    else:
        # Display the form with current employer profile details for GET requests
        form = EmployerEditForm(instance=employer)

    return render(request, 'company_profile.html', {'employer': employer, 'form': form})

@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            # Create a new JobPosting instance with the form data
            job_posting = form.save(commit=False)

            # Set the employer based on the logged-in user
            job_posting.employer = request.user.userprofile.employer

            # Save the job posting
            job_posting.save()

            messages.success(request, 'Job posted successfully!')
            return redirect('post_job')  # Redirect to the same page or another if needed
    else:
        # If it's a GET request, create a new form
        form = JobPostingForm()

    return render(request, 'post_job.html', {'form': form})

def dashboard(request):
    return render(request, 'dashboard.html', {})

def dashboard_post(request):
    job_postings = JobPosting.objects.all()  # Or apply any filtering you need
    return render(request, 'dashboard_post.html', {'job_postings': job_postings})