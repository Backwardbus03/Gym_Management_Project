from django.contrib.auth.decorators import login_required
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
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']  # this is crucial!
        if commit:
            user.save()
        return user

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect based on the role
            if user.role == 'trainer':
                return redirect('trainers')
            elif user.role == 'trainee':
                return redirect('trainees')
            elif user.role == 'admin':
                return redirect('/admin/')  # or your custom admin dashboard
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'users/role_login_redirect.html')

def user_logout(request):
    logout(request)
    return redirect('users/login')

def index(request):
    return render(request, 'users/home.html')

@login_required
def delete_account(request):
    if request.method == 'POST':
        if request.POST.get('confirm_delete') == 'yes':
            # Store username for confirmation message
            username = request.user.username

            # Log the user out first
            user = request.user
            logout(request)

            # Delete the user account
            user.delete()

            # Show success message
            messages.success(request, f"Account '{username}' has been permanently deleted.")
            return redirect('home')  # Redirect to home page
        else:
            # User didn't confirm deletion
            return redirect('dashboard')  # Redirect back to dashboard

    return render(request, 'users/delete_account.html')
