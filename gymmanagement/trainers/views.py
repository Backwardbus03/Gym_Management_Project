from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django import forms
from users.models import CustomUser
from .models import Trainer
from django.core.exceptions import ValidationError


class TrainerSignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    age = forms.IntegerField()
    experience = forms.IntegerField()
    specialisation = forms.CharField(max_length=100)
    rate = forms.FloatField()
    start_time = forms.TimeField()
    end_time = forms.TimeField()


def trainer_signup(request):
    if request.method == 'POST':
        form = TrainerSignupForm(request.POST)
        if form.is_valid():
            try:
                # 1. Create the CustomUser with role='trainer'
                user = CustomUser.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    role='trainer'
                )

                # 2. Create Trainer Profile
                trainer = Trainer(
                    user=user,
                    age=form.cleaned_data['age'],
                    experience=form.cleaned_data['experience'],
                    specialisation=form.cleaned_data['specialisation'],
                    rate=form.cleaned_data['rate'],
                    start_time=form.cleaned_data['start_time'],
                    end_time=form.cleaned_data['end_time'],
                )

                # 3. Run model validation (custom clean methods)
                trainer.full_clean()
                trainer.save()

                # 4. Log the user in and redirect
                login(request, user)
                return redirect('trainer_dashboard')

            except ValidationError as ve:
                user.delete()  # rollback if the profile fails
                form.add_error(None, ve.message_dict)

            except Exception as e:
                form.add_error(None, f"An unexpected error occurred: {str(e)}")
        else:
            messages.error(request, "Please fix the form errors below.")
    else:
        form = TrainerSignupForm()

    return render(request, 'trainers/signup.html', {'form': form})

def trainer_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.role == 'trainer':
            login(request, user)
            return redirect('trainer_dashboard')
        else:
            messages.error(request, 'Invalid trainer credentials')
    return render(request, 'trainers/login.html')

@login_required
def dashboard(request):
    return render(request, 'trainers/trainers.html')