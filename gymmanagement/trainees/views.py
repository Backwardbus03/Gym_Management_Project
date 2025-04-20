from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django import forms
from users.models import CustomUser
from .models import Trainee
from django.core.exceptions import ValidationError


class TraineeSignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    trainer = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='trainer'),
        required=False,
        empty_label='No trainer'
    )


def trainee_signup(request):
    if request.method == 'POST':
        form = TraineeSignupForm(request.POST)
        if form.is_valid():
            try:
                # 1. Create the CustomUser with role='trainee'
                user = CustomUser.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    role='trainee'
                )

                # 2. Create Trainee Profile
                trainee = Trainee(
                    user=user,
                    trainer=form.cleaned_data['trainer']
                )

                # 3. Run model validation (custom clean methods)
                trainee.full_clean()
                trainee.save()

                # 4. Log the user in and redirect
                login(request, user)
                return redirect('trainee_dashboard')

            except ValidationError as ve:
                user.delete()  # rollback if the profile fails
                form.add_error(None, ve.message_dict)

            except Exception as e:
                form.add_error(None, f"An unexpected error occurred: {str(e)}")
        else:
            messages.error(request, "Please fix the form errors below.")
    else:
        form = TraineeSignupForm()

    return render(request, 'trainees/signup.html', {'form': form})

def trainee_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.role == 'trainee':
            login(request, user)
            return redirect('trainee_dashboard')
        else:
            messages.error(request, 'Invalid trainee credentials')
    return render(request, 'trainees/login.html')

@login_required
def dashboard(request):
    return render(request, 'trainees/trainees.html')
