from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *

class CustomSignupForm(UserCreationForm):
    ROLE_CHOICES = (
        ('trainer', 'Trainer'),
        ('trainee', 'Trainee'),
        ('admin', 'Admin')
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']

def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users/login')
    else:
        form = CustomSignupForm()
    return render(request, 'users/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect based on role
            if user.role == 'trainer':
                return redirect('trainers')
            elif user.role == 'trainee':
                return redirect('trainees')
            elif user.role == 'admin':
                return redirect('/admin/')  # or your custom admin dashboard
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'users/ai_login.html')

def user_logout(request):
    logout(request)
    return redirect('users/login')

def index(request):
    return render(request, 'users/home.html')
