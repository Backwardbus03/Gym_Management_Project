from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django import forms
from users.models import CustomUser
from trainers.models import Recommendation
from django.core.exceptions import ValidationError
from django.shortcuts import render
from .models import Trainee, Activity, WorkoutTarget, WeightLog
from django.contrib.auth.decorators import login_required
from datetime import timedelta, date
from .forms import *
from django.utils.timezone import now


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

def generate_recommendation(trainee):
    last_activity = Activity.objects.filter(trainee=trainee).order_by('-date').first()
    if not last_activity:
        return "Start light today with some cardio!"
    if last_activity.name.lower() == 'treadmill' and last_activity.duration_minutes > 30:
        return "Go easy today. Try yoga or stretching."
    elif last_activity.name.lower() == 'weightlifting':
        return "Consider a light cardio session today."
    return "Keep up the good work!"

@login_required
def trainee_dashboard(request):
    trainee = request.user.trainee_profile
    today = now().date()
    one_week_ago = today - timedelta(days=7)

    activities = Activity.objects.filter(trainee=trainee, date__gte=one_week_ago)
    weight_logs = WeightLog.objects.filter(trainee=trainee).order_by('-date')[:5]

    weekly_minutes = sum(a.duration_minutes for a in activities)
    weekly_calories = sum(a.calories_burned for a in activities)

    # Trainer recommendation for today
    today_recommendation = Recommendation.objects.filter(
        trainee=trainee,
        created_at__date=today
    ).order_by('-created_at').first()

    if today_recommendation:
        recommendation = today_recommendation.message
    else:
        recommendation = generate_recommendation(trainee)

    context = {
        'weekly_minutes': weekly_minutes,
        'weekly_calories': weekly_calories,
        'weight_logs': weight_logs,
        'recommendation': recommendation,
    }

    return render(request, 'trainees/dashboard.html', context)

@login_required
def log_activity(request):
    trainee = request.user.trainee_profile
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.trainee = trainee
            activity.save()
            return redirect('trainee_dashboard')
    else:
        form = ActivityForm()
    return render(request, 'trainees/log_activity.html', {'form': form})

@login_required
def log_weight(request):
    trainee = request.user.trainee_profile
    if request.method == 'POST':
        form = WeightLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.trainee = trainee
            log.save()
            return redirect('trainee_dashboard')
    else:
        form = WeightLogForm()
    return render(request, 'trainees/log_weight.html', {'form': form})