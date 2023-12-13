from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CreateUserForm, UserCVForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from .forms import UserProfileEditForm, EmployerEditForm, JobPostingForm, GraduateTracerForm
from django.views import View
from django.db import IntegrityError
from .models import UserProfile, Employer, JobPosting, UserCV, GraduateTracer
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.admin.views.decorators import staff_member_required

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
        job_postings = employer.job_postings.all()
    except Employer.DoesNotExist:
        # Handle the case where the Employer profile doesn't exist
        employer = None
        job_postings = None

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

    return render(request, 'company_profile.html', {'employer': employer, 'form': form, 'job_postings': job_postings})

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
    filter_value = request.GET.get('filter', 'all')

    if filter_value == 'verified':
        job_postings = JobPosting.objects.filter(is_verified=True)
    elif filter_value == 'unverified':
        job_postings = JobPosting.objects.filter(is_verified=False)
    else:
        job_postings = JobPosting.objects.all()

    context = {
        'job_postings': job_postings,
        'filter': filter_value,
    }
    return render(request, 'dashboard_post.html', context)

@staff_member_required
def delete_job_post(request, job_post_id):
    job_post = get_object_or_404(JobPosting, id=job_post_id)

    # Check if the user is a staff member
    if request.user.is_staff:
        job_post.delete()

        return redirect('dashboard_post')

    return HttpResponseForbidden("You don't have permission to perform this action.")

@staff_member_required
def verify_job_post(request, job_post_id):
    job_post = get_object_or_404(JobPosting, id=job_post_id)

    # Check if the user is a staff member
    if request.user.is_staff:
        job_post.is_verified = True
        job_post.save()

        return redirect('dashboard_post')

    return HttpResponseForbidden("You don't have permission to perform this action.")

@login_required
def dashboard_users(request):
    users = User.objects.all().exclude(username=request.user.username)  # Exclude the currently logged-in user
    return render(request, 'dashboard_users.html', {'users': users})

@login_required
def delete_user(request, username):
    user = get_object_or_404(User, username=username)
    
    if request.method == 'POST':
        # Perform the deletion logic here
        user.delete()
        return redirect('dashboard_users')
    
    return render(request, 'confirm_delete_user.html', {'user': user})


def job_find(request):
    # Fetch only verified job postings
    verified_job_postings = JobPosting.objects.filter(is_verified=True)

    context = {
        'verified_job_postings': verified_job_postings,
    }

    return render(request, 'job_find.html', context)

def job_info(request, job_post_id):
    job_posting = get_object_or_404(JobPosting, id=job_post_id)
    user = request.user

    already_applied = False  # Default value, assuming the user is not authenticated

    if user.is_authenticated:
        already_applied = UserCV.objects.filter(user=user, job_posting=job_posting).exists()

    # You can customize the context data based on your needs
    context = {'job_posting': job_posting, 'already_applied': already_applied}
    return render(request, 'job_info.html', context)

def apply_job(request, job_posting_id):
    job_posting = get_object_or_404(JobPosting, pk=job_posting_id)
    
    if request.method == 'POST':
        form = UserCVForm(request.POST, request.FILES)
        if form.is_valid():
            user_cv = form.save(commit=False)
            user_cv.user = request.user  # Assuming you are using authentication
            user_cv.job_posting = job_posting
            user_cv.company_name = job_posting.employer.company_name
            user_cv.save()
            return redirect('home')  # Redirect to a success page or another appropriate view
    else:
        form = UserCVForm()

    return render(request, 'job_info.html', {'job_posting': job_posting, 'form': form})

def view_applications(request, job_post_id):
    job_posting = get_object_or_404(JobPosting, id=job_post_id)
    # Add logic to retrieve and display job applications
    return render(request, 'view_applications.html', {'job_posting': job_posting})

@login_required
def graduate_tracer(request):
    existing_record = GraduateTracer.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = GraduateTracerForm(request.POST, instance=existing_record)
        if form.is_valid():
            graduate_tracer_instance = form.save(commit=False)
            graduate_tracer_instance.user = request.user
            graduate_tracer_instance.save()
            return redirect('profile', username=request.user)
    else:
        form = GraduateTracerForm(instance=existing_record)

    return render(request, 'graduate_tracer.html', {'form': form})