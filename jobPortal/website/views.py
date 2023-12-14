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
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import ObjectDoesNotExist

def home(request):
    return render(request, 'home.html', {})

def about(request):

    user_count = User.objects.count()
    job_posting_count = JobPosting.objects.count()
    employer_count = Employer.objects.count()

    context = {
        'user_count': user_count,
        'job_posting_count': job_posting_count,
        'employer_count': employer_count,
    }

    return render(request, 'about.html', context)

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
def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, request.FILES, instance=user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=user.id)  # Redirect to the profile page after saving
    else:
        form = UserProfileEditForm(instance=user.userprofile)

    return render(request, 'profile.html', {'user': user, 'form': form})

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
    # Get counts from the database
    user_count = User.objects.count()
    job_posting_count = JobPosting.objects.count()
    employer_count = Employer.objects.count()

    # Pass the counts to the template
    context = {
        'user_count': user_count,
        'job_posting_count': job_posting_count,
        'employer_count': employer_count,
    }

    return render(request, 'dashboard.html', context)

def dashboard_post(request):
    filter_value = request.GET.get('filter', 'all')

    if filter_value == 'verified':
        job_postings_verified = JobPosting.objects.filter(is_verified=True)
        job_postings_unverified = JobPosting.objects.filter(is_verified=True)
    elif filter_value == 'unverified':
        job_postings_verified = []
        job_postings_unverified = JobPosting.objects.filter(is_verified=False)
    else:
        job_postings_verified = JobPosting.objects.filter(is_verified=True)
        job_postings_unverified = JobPosting.objects.filter(is_verified=False)

    # Concatenate the two querysets, placing unverified ones first
    job_postings = list(job_postings_unverified) + list(job_postings_verified)

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

    # Paginate the verified job postings
    page = request.GET.get('page', 1)
    paginator = Paginator(verified_job_postings, 10)  # Show 5 jobs per page

    try:
        verified_job_postings = paginator.page(page)
    except PageNotAnInteger:
        verified_job_postings = paginator.page(1)
    except EmptyPage:
        verified_job_postings = paginator.page(paginator.num_pages)

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

@login_required
def dashboard_tracer(request):
    # Retrieve all GraduateTracer instances
    graduate_tracers = GraduateTracer.objects.all()

    context = {'graduate_tracers': graduate_tracers}
    return render(request, 'dashboard_tracer.html', context)

@login_required
def delete_tracer(request, username):
    # Ensure the user has the permission to delete
    if request.user.is_staff:
        # Retrieve the user associated with the GraduateTracer instance
        user = get_object_or_404(User, username=username)

        # Delete the GraduateTracer instance associated with the user
        try:
            graduate_tracer = GraduateTracer.objects.get(user=user)
            graduate_tracer.delete()
            messages.success(request, f'GraduateTracer for {username} has been deleted.')
        except GraduateTracer.DoesNotExist:
            messages.error(request, f'GraduateTracer for {username} does not exist.')

    return redirect('dashboard_tracer')

#? Generator

class SearchJobsView(View):
    template_name = 'job_find.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        job_postings = JobPosting.objects.filter(job_title__icontains=query) | \
                        JobPosting.objects.filter(employer__company_name__icontains=query)

        context = {
            'verified_job_postings': job_postings,
            'query': query,
        }

        return render(request, self.template_name, context)
    
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def recommend_jobs(request):

    user_count = User.objects.count()
    job_posting_count = JobPosting.objects.count()
    employer_count = Employer.objects.count()
    
    try:
        user_id = request.user.id
        user_profile = UserProfile.objects.get(user=user_id)
        user_skill_description = user_profile.skill_description

        job_postings = list(JobPosting.objects.filter(is_verified=True))

        user_count = User.objects.count()
        job_posting_count = JobPosting.objects.count()
        employer_count = Employer.objects.count()

        # Check if user_skill_description is not None
        if user_skill_description:
            # Check if any job_requirements are not None
            job_requirements_list = [job.job_requirements for job in job_postings if job.job_requirements]

            # Check if there are any job_requirements before vectorization
            if job_requirements_list:
                # Calculate TF-IDF vectors for skill_description and job_requirements
                documents = [user_skill_description] + job_requirements_list
                vectorizer = TfidfVectorizer()
                tfidf_matrix = vectorizer.fit_transform(documents)

                # Calculate cosine similarity between user's skill_description and job_requirements
                similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])

                # Get the indices of job postings sorted by similarity (descending order)
                recommended_job_indices = similarity_scores.argsort()[0][::-1]

                # Filter out indices that are out of range
                valid_indices = [index for index in recommended_job_indices if 0 <= index < len(job_postings)]

                # Get the recommended job postings
                recommended_job_postings = [job_postings[index] for index in valid_indices]

            else:
                recommended_job_postings = []

        else:
            recommended_job_postings = []

    except ObjectDoesNotExist:
        # Handle the case where the UserProfile does not exist
        # You can also set recommended_job_postings to an empty list or provide default recommendations
        recommended_job_postings = []

    context = {
        'recommended_job_postings': recommended_job_postings,
        'user_count': user_count,
        'job_posting_count': job_posting_count,
        'employer_count': employer_count,
    }

    return render(request, 'home.html', context)


