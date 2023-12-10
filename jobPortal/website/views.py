from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CreateUserForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from .forms import UserProfileEditForm
from django.views import View


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