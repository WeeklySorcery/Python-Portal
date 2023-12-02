from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
import random

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

def generate_unique_username(first_name, last_name):
    # Combine the first name, last name, and a random number
    username = f"{first_name}{last_name}#{random.randint(100000, 999999)}"
    return username

def signup(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = generate_unique_username(user.first_name, user.last_name)  # Implement a function to generate a unique username
            user.save()
            auth_login(request, user)
            return redirect('home')  # Redirect to home or any other desired page
    else:
        form = CreateUserForm()

    return render(request, 'signup.html', {'form': form})
